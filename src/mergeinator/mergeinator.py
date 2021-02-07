#!/usr/bin/env python3

import os
import re
import shutil
import stat
import sys

from datetime import datetime as dt
from subprocess import run, STDOUT, PIPE, Popen, TimeoutExpired

from .logs import BLD, GRN, WHT, YEL, RED, NORMAL, DIM


SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 60 * SECONDS_IN_MINUTE
SECONDS_IN_DAY = 24 * SECONDS_IN_HOUR
SECONDS_IN_WEEK = 7 * SECONDS_IN_DAY
# These are approximate:
SECONDS_IN_MONTH = 30 * SECONDS_IN_DAY
SECONDS_IN_YEAR = 365 * SECONDS_IN_DAY


def log(*args, **kwargs):
    mode = "w+"
    if os.path.isfile("merge.log"):
        mode = "a"
    with open("merge.log", mode) as global_log:
        print(dt.isoformat(dt.now()), *args, file=global_log, **kwargs)


def ui(*args, **kwargs):
    print(*args, **kwargs)
    log(*args, **kwargs)


def nicedelta(delta_s):
    """Return an approximate nice looking time delta string from delta (in seconds).

    To be exact, we would need the two actual dates, rather than the number of seconds
    between them.
    """

    years = int(delta_s / SECONDS_IN_YEAR)
    remainder = delta_s - (years * SECONDS_IN_YEAR)

    months = int(remainder / SECONDS_IN_MONTH)
    remainder -= months * SECONDS_IN_MONTH

    weeks = int(remainder / SECONDS_IN_WEEK)
    remainder -= weeks * SECONDS_IN_WEEK

    days = int(remainder / SECONDS_IN_DAY)
    remainder -= days * SECONDS_IN_DAY

    hours = int(remainder / SECONDS_IN_HOUR)
    remainder -= hours * SECONDS_IN_HOUR

    minutes = int(remainder / SECONDS_IN_MINUTE)
    remainder -= minutes * SECONDS_IN_MINUTE

    # Round to tenths of a second
    seconds = int(remainder * 10) / 10
    remainder -= int(seconds)

    if delta_s < 0.1:
        milliseconds = int(remainder * 1000)
        remainder -= milliseconds * 1000
        # Round to tenths of a microsecond
        microseconds = int(remainder * 10e6 * 10) / 10

    if delta_s < 0.01:
        return "infinitesimal "

    str = ""
    if years > 0:
        str = f"{years}Y "
    if months > 0:
        str += f"{months}M "
    if weeks > 0:
        str += f"{weeks}W "
    if days > 0:
        str += f"{days}d "
    if hours > 0:
        str += f"{hours}h "
    if minutes > 0:
        str += f"{minutes}m "
    if seconds > 0:
        str += f"{seconds}s "
    if not len(str) > 0:
        if milliseconds > 0:
            str += f"{milliseconds}ms "
        if not len(str) > 0:
            str += f"{microseconds}usec "
    return str


KB = 1024
MB = 1024 * KB
GB = 1024 * MB
# TB = 1024 * GB
# PB = 1024 * TB
# EB = 1024 * PB


def nice_size(bytes):
    """Report bytes in appropriate units for size: T, G, M, K."""
    if bytes > GB:
        return f"{int(bytes*GB/10)/10} GB"
    if bytes > MB:
        return f"{int(bytes*MB/10)/10} MB"
    if bytes > KB:
        return f"{int(bytes*10/KB)/10} KB"
    return f"{bytes}B"


def answer(question):
    global force_yes
    global dry_run
    retval = 'n'
    if dry_run:
        print(question, BLD + GRN + "n" + NORMAL)
    if force_yes:
        print(question, BLD + RED + "y" + NORMAL)
        retval = 'y'
    else:
        retval = str.lower(input(question))
    log(question, retval)
    return retval


def not_dead_gen():
    """I'm not dead, Jim"""
    spinner_state = 0
    spinner_map = ['|', '/', '-', '\\']

    while True:
        # Two chars so spinner doesn't end up under cursor
        print(f" {spinner_map[spinner_state]}\b\b", end='')
        sys.stdout.flush()
        spinner_state = (spinner_state + 1) % len(spinner_map)
        yield


def unstick(file):
    """Make an attempt to make FILE readable and deleteable."""

    def my_run(cmd):
        ui(f"Running {cmd}")
        result = run([cmd])
        ui(f"Result: {result.returncode}")
        return result.returncode

    def examine(file):
        return my_run(["ls", "-dle@O", file])

    ret = examine(file)
    if ret.returncode == 0:
        path_to_fix = file
    if ret.returncode == 1:
        # ls didn't even work.  Try to fix the parent dir.
        path_to_fix = os.path.dirname(file)
        ret = examine(dirname)

    my_run(["chmod", "u+rwx", path_to_fix])
    my_run(["chmod", "-RN", path_to_fix])

    # Maybe it worked?
    return True



def safe_len(path):
    if not os.path.isdir(path):
        ui(f"{path} isn't a directory.")
        return -1
    try:
        listing = os.listdir(path)
    except PermissionError as e:
        ui(f"Couldn't list {path} due to permission error.")
        unstick(path)
        ui(f"It might work to retry now.")
        sys.exit(1)
    return len(listing)

def identical(f1, f2):
    """Return true iff paths f1 and f2 have no diffs.

    Don't count permission differences.
    Prints a spinner while polling the diff for completion.
    """

    # If one path is a directory and the other is a file, they aren't identical.
    # Also, we have to check this case, because diff will fail on it.
    if not os.path.isdir(f1) == os.path.isdir(f2):
        ui("Weird Case: one dir, one non-dir")
        return False

    # Cheap shortcut: If two directories contain different numbers of items,
    # they aren't identical.
    if os.path.isdir(f1) and os.path.isdir(f2):
        if safe_len(f1) != safe_len(f2):
            return False

    not_dead = not_dead_gen()

    ui(f"{DIM}Diff {WHT}{f1}...{NORMAL}")
    # TODO: If diff doesn't support --no-dereference, print warning
    # that it will fail on symlinks with no referent.
    cmd = ["/usr/local/bin/diff", "-r", "--no-dereference", "-q", f1, f2]
    log(f"{DIM}{WHT}Diff cmd: {cmd}...{NORMAL}")
    sofar = bytearray(b'')
    chunk = bytearray(b'')
    import io
    # ui(f"io.DEF {io.DEFAULT_BUFFER_SIZE}.")
    with Popen(cmd, stdout=PIPE, stderr=PIPE, bufsize=100 * io.DEFAULT_BUFFER_SIZE) as p:
        ret = None
        # ui("Popened.")
        while ret is None:
            try:
                (chunk, bunk) = p.communicate(timeout=0.1)
                # ui("Chunk: ", chunk, ".")
                # ui("Bunk: ", bunk, ".")
                if len(chunk) > 0:
                    sofar.extend(chunk)
                    chunk = bytearray(b'')
            except TimeoutExpired:
                # Maybe need to read last chunk?
                pass
            # Prints next spinner char
            next(not_dead)
            ret = p.poll()

        sofar.extend(chunk)
        if ret == 2:
            ui(f"{DIM}{YEL}ret {ret}, output {sofar}{NORMAL}")
            ui(f"{RED}Diff returned an unexpected error.{NORMAL}.")
            err_msg = bunk.decode()
            ui(f"  While running \"{' '.join(cmd)}\", error was:\n"
               f"  {YEL}{err_msg}{YEL}.\n")
            if not "Permission denied" in err_msg:
                sys.exit(1)
            ui("Continuing after permission error.")
        # If there is a difference (or an error), ret will be nonzero
        match = ret == 0
    return match


def _dmark(path):
    """Return a mark that indicates file type, or "" for ordinary files.

    Returns a slash (`/') if the path is a directory, an asterisk (`*') for executables, an
    at sign (`@') for symbolic links, an equals sign (`=') for sockets, a
    percent sign (`%') whiteouts, or a vertical bar (`|') for a FIFO.
    """

    if not os.path.exists(path):
        return ""
    elif os.path.isdir(path):
        return "/"
    elif os.path.isfile(path) and os.access(path, os.X_OK):
        return "*"
    elif os.path.islink(path):
        return"@"
    elif stat.S_ISSOCK(os.stat(path).st_mode):
        return "="
    elif stat.S_ISWHT(os.stat(path).st_mode):
        return "%"
    elif stat.S_ISFIFO(os.stat(path).st_mode):
        return "|"
    else:
        return ""


def _mark(path):
    """Return path with a type indication appended."""
    return path + _dmark(path)


def printfiles(f1, f2, mod1, mod2):
    """Print source and destination file with mod1 and mod2.

    Args:
        f1, f2: filenames to print.
        mod1, mod2: color/bold/dim modifier
    """
    ui(f"{mod1}{f1}{_dmark(f1)}{NORMAL} ?--> {mod2}{f2}{_dmark(f2)}{NORMAL}", end="")


def remove(path):
    """Remove path, whether it's a file or a directory (and its contents)."""
    deleter = os.remove
    mpath = _mark(path)
    if os.path.islink(path):
        log(f"Deleting link {mpath}")
    elif os.path.isfile(path):
        log(f"Deleting file {mpath}")
    elif os.path.isdir(path):
        log(f"Deleting dir {mpath}")
        deleter = shutil.rmtree
    else:
        ui(f"Don't know how to delete {mpath}!")
        sys.exit(1)
    try:
        deleter(path)
    except PermissionError as e:
        if e.args[1] == "Operation not permitted":
            # Empirically, this has been due to MacOS uchg.
            # It could also be locked with xattrs.
            try:
                # TODO:  Call chflags(2) directly
                run(["chflags", "-R", "nouchg", path])
                deleter(path)
                ui(f"Deleted {path} after removing nouchg.")
            except PermissionError as fuu:
                ui(f"Couldn't delete {mpath}: {e} and {fuu}")


def move(src, dest):
    # ui(f"{DIM}Moving {WHT}{_mark(src)}{NORMAL}{DIM} to {dest_abbrev}{NORMAL}")
    log(f"Moving {WHT}{_mark(src)}{NORMAL} to {dest_abbrev}")
    try:
        shutil.move(src, dest)
    except FileExistsError as e:
        # ui(f"Uh. . . .  {e}, {dir(e)}")
        # ui(f"Errno: {e.errno}, filename: {e.filename} args: {e.args}")
        if os.path.islink(dest) and not os.path.exists(dest):
            ui(f"Destination {_mark(dest)} is a symlink that points nowhere.  "
               f"{RED}Skipping{NORMAL}.")
        else:
            raise(e)
    except PermissionError as e:
        ui(f"{RED}Yo, Move Permission Error.{NORMAL}")
        if unstick(src):
            ui("It could possibly work to re-run.")
        ui("Bye for now.")
        sys.exit(1)
    except Exception as e:
        ui(f"{RED}Ah HA!")
        raise(e)




def finderopen(path):
    run(["open", "-R", path])


def is_empty(path):
    """Return true for zero length files and empty directories."""

    if os.path.isfile(path):
        if os.path.getsize(path) == 0:
            return True
    if os.path.isdir(path):
        try:
            files = os.listdir(path)
        except PermissionError as e:
            ui(f"Can't list dir {WHT}{path}{NORMAL}: {YEL}{e}{NORMAL}")
            unstick(path)
            sys.exit(1)
        if len(files) == 0:
            return True
    return False


def do_merge(src, dest, level, dry_run_flag, yes_flag):
    """Top-level call from CLI, set global flags and call initial walk()."""

    global force_yes
    global dry_run
    global dest_dir
    global dest_abbrev
    force_yes = yes_flag
    dry_run = dry_run_flag
    dest_dir = dest
    dest_abbrev = dest_dir + "/. . ."
    walk(src, dest_dir, level)


def walk(src_dir, dest_dir, level):
    """For each file in this directory, dispose of it sensibly.

    If it doesn't exist in the destination, offer to move it.
    If it's empty or a symlink, offer to delete it.
    If it's identical, offer to delete it.
    If it differs, report the details and make an offer."""

    for fname in os.listdir(src_dir):
        abs_f = os.path.normpath(os.path.join(src_dir, fname))
        dest_file = os.path.normpath(os.path.join(dest_dir, fname))
        if not os.path.exists(dest_file):
            printfiles(abs_f, dest_abbrev, WHT, DIM)
            safe_move = answer("  Safe.  Move? [Y/n]")
            if safe_move in ["", "y"]:
                move(abs_f, dest_file)
                continue
        elif is_empty(abs_f) or os.path.islink(abs_f):
            if is_empty(abs_f):
                reason = "empty"
            else:
                reason = "symlink"
            del_ok = answer(f"{abs_f} is {reason}.  Delete? [Y/D/n]")
            if del_ok in ["", "y", "d"]:
                remove(abs_f)
                continue
        elif identical(abs_f, dest_file):
            printfiles(abs_f, dest_abbrev, WHT, "")
            ui("  Identical.", end="")
            merge = answer("  Delete? [Y/n]")
            if merge in ["", "y"]:
                remove(abs_f)
                continue
            else:
                ui(f"Left {abs_f}.")
        else:
            printfiles(abs_f, dest_abbrev, WHT, YEL)
            ui("  Differs.")

            # Check mod times
            abs_f_mtime = os.path.getmtime(abs_f)
            dest_f_mtime = os.path.getmtime(dest_file)
            ds = dt.fromtimestamp(dest_f_mtime)
            readable_date = ds.strftime("%Y-%m-%d %H:%M:%S")
            if abs_f_mtime == dest_f_mtime:
                ui(f"Both have the same modification time ({abs_f_mtime}).")
            else:
                diff = abs(abs_f_mtime - dest_f_mtime)
                amount = nicedelta(diff)
                if abs_f_mtime > dest_f_mtime:
                    op = "newer"
                else:
                    op = "older"
                    ui(f"{WHT}{_mark(abs_f)}{NORMAL} is {amount} {op} than "
                       f"{YEL}{dest_abbrev}{NORMAL} ({readable_date}).")

            # Check for directories we shouldn't open
            dirtype = re.match(".*\\.git$|.*\\.xcodeproj$|.*\\.nib$", abs_f)

            # Report size
            if os.path.isfile(abs_f):
                asize = os.path.getsize(abs_f)
                dsize = os.path.getsize(dest_file)
                if asize == dsize:
                    ui(f"Both are {nice_size(asize)}.")
                else:
                    ui(f"{WHT}{abs_f}{NORMAL} is {nice_size(asize)}, "
                       f"{YEL}{dest_abbrev}{NORMAL} is {nice_size(dsize)}.")

            # If this is a flatfile or monolithic directory, offer to delete older
            if os.path.isfile(abs_f) or dirtype:
                if abs_f_mtime > dest_f_mtime:
                    older_file = dest_file
                else:
                    older_file = abs_f
                del_ok = "d"
                while del_ok == 'd':
                    del_ok = answer(f"[R]emove older file ({older_file + _dmark(older_file)}) "
                                    "or show [d]iff [R/n/d]?")
                    if del_ok == 'd':
                        ui("\n{BOLD}Showing Diff{NORMAL}")
                        rv = run(["diff", "-r", abs_f, dest_file], capture_output=True)
                        ui(rv.stdout)
                    if del_ok in ['', 'r', 'y']:
                        remove(older_file)
                        continue
                    if del_ok == 'n':
                        pass
            if os.path.isdir(abs_f):
                # Weird case: Source dir, dest file
                if not os.path.isdir(dest_file):
                    ui(f"{WHT}{abs_f}{NORMAL} is a dir with {abs_f_entries} files, "
                       f"{dest_abbrev} is a plain file.  Not sure what to do.")
                    sys.exit();
                abs_f_entries = len(os.listdir(abs_f))
                dest_entries = len(os.listdir(dest_file))
                ui(f"{WHT}{abs_f}{NORMAL} has {abs_f_entries} files, "
                   f"{dest_abbrev} has {dest_entries}.")

                # Ask for help
                if os.path.isdir(abs_f):
                    action = answer("[C]heck inside, [o]pen in finder, or [s]kip [Cos]?")
                    if action in ["y", "c", ""]:
                        walk(abs_f, dest_file, level + 1)
                    elif action == "o":
                        finderopen(abs_f)
                        finderopen(dest_file)
                    elif action == "s":
                        ui("Skipping.")
