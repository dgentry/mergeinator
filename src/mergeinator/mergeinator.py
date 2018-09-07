#!/usr/bin/env python3

import datetime
import sys
import stat
import subprocess
import os
import re
import shutil
from sys import stdout
from colored import fg, style

# Let's use ANSI escape sequence colors if we're on a tty
if stdout.isatty() or ('TERM' in os.environ and 'color' in os.environ['TERM']):
    WHT = fg('white')
    GRN = fg('green')
    YEL = fg('yellow')
    RED = fg('red')
    BLD = style.BOLD
    NORMAL = style.RESET
    RESET = "\x1b[39m"
    DIM = style.DIM
# But don't pollute a logfile with escape sequences
else:
    WHT = ''
    GRN = ''
    YEL = ''
    RED = ''
    BLD = ''
    NORMAL = ''
    RESET = ''
    DIM = ''
BLDWHT = BLD + WHT
BLDRED = BLD + RED

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 60 * SECONDS_IN_MINUTE
SECONDS_IN_DAY = 24 * SECONDS_IN_HOUR
SECONDS_IN_WEEK = 7 * SECONDS_IN_DAY
# These are approximate:
SECONDS_IN_MONTH = 30 * SECONDS_IN_DAY
SECONDS_IN_YEAR = 365 * SECONDS_IN_DAY


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
    if dry_run:
        print(question, BLD + GRN + "n" + NORMAL)
        return "n"
    if force_yes:
        print(question, BLD + RED + "y" + NORMAL)
        return "y"
    else:
        return str.lower(input(question))


def identical(f1, f2):
    """Return true iff paths f1 and f2 have no diffs.

    Permission differences don't count.
    """

    cp = subprocess.run(["diff", "-r", "-q", f1, f2], capture_output=True)
    match = len(cp.stdout) == 0 and len(cp.stderr) == 0
    # if not match:
    #     print(WHT + f"{len(cp.stdout)}, {len(cp.stderr)}{cp.stderr}\n" + RESET)
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


def printfiles(level, f1, f2, mod):
    """Indent according to level, then print source and destination file nicely.

    Args:
        level: depth from root in source tree.
        f1, f2:  filenames to print.
        mod:  color/bold/dim modifier
    """
    print(" " * level * 4 + f"{f1}{_dmark(f1)} ?--> {mod}{f2}{_dmark(f2)}{NORMAL}", end="")


def remove(path):
    """Remove whatever path is (file or directory and its contents)."""
    if os.path.islink(path):
        print(f"Deleting link {path}.")
        os.remove(path)
    elif os.path.isfile(path):
        print(f"Deleting file {path}.")
        os.remove(path)
    elif os.path.isdir(path):
        print(f"Deleting dir {path}/.")
        shutil.rmtree(path)
    else:
        print(f"Don't know how to delete {path}!")
        sys.exit(1)


def move(src, dst):
    print(f"Moving {src} to {dst}.")
    shutil.move(src, dst)


def finderopen(path):
    subprocess.run(["open", "-R", path])


def is_empty(path):
    """Return true for zero length files and empty directories."""

    if os.path.isfile(path):
        if os.path.getsize(path) == 0:
            return True
    if os.path.isdir(path):
        files = os.listdir(path)
        if len(files) == 0:
            return True
    return False


def do_merge(root_dir, dest_root, level, dry_run_flag, yes_flag):
    """Set global flags and call initial walk()."""

    global force_yes
    global dry_run
    force_yes = yes_flag
    dry_run = dry_run_flag
    walk(root_dir, dest_root, level)


def walk(root_dir, dest_root, level):
    """For each file in this directory, if it matches the one in the merge destination, offer to
    delete it."""

    for fname in os.listdir(root_dir):
        abs_f = os.path.normpath(os.path.join(root_dir, fname))
        dest_file = os.path.normpath(os.path.join(dest_root, fname))
        if not os.path.exists(dest_file):
            printfiles(level, abs_f, dest_file, DIM)
            safe_move = answer("  Safe.  Move? [Y/n]")
            if safe_move in ["", "y"]:
                move(abs_f, dest_file)
                continue
        elif identical(abs_f, dest_file):
            printfiles(level, abs_f, dest_file, "")
            print("  Identical.", end="")
            merge = answer("  Delete? [Y/n]")
            if merge in ["", "y"]:
                remove(abs_f)
                continue
            else:
                print("")
        else:
            printfiles(level, abs_f, dest_file, RED)
            print("  Differs.")

            # Check for source empty or symlink
            reason = ""
            if is_empty(abs_f):
                reason = "empty"
            elif os.path.islink(abs_f):
                reason = "a symlink"
            if len(reason) > 0:
                del_ok = answer(f"{abs_f} is {reason}.  Delete? [Y/D/n]")
                if del_ok in ["", "y", "d"]:
                    remove(abs_f)
                    continue

            # Check mod times
            abs_f_mtime = os.path.getmtime(abs_f)
            dest_f_mtime = os.path.getmtime(dest_file)
            dt = datetime.datetime.fromtimestamp(dest_f_mtime)
            readable_date = dt.strftime("%Y-%m-%d %H:%M:%S")
            if abs_f_mtime == dest_f_mtime:
                print(f"Both files have the same modification time ({abs_f_mtime}).")
            else:
                diff = abs(abs_f_mtime - dest_f_mtime)
                amount = nicedelta(diff)
                if abs_f_mtime > dest_f_mtime:
                    op = "newer"
                else:
                    op = "older"
                print(f"{abs_f} is {amount}seconds {op} than {dest_file}{_dmark(dest_file)} "
                      f"({readable_date}).")

            # Check for directories we shouldn't open
            dirtype = re.match(".*\.git$|.*\.xcodeproj$", abs_f)

            # Report size
            if os.path.isfile(abs_f):
                asize = os.path.getsize(abs_f)
                dsize = os.path.getsize(dest_file)
                if asize == dsize:
                    print(f"Both are {nice_size(asize)}.")
                else:
                    print(f"{abs_f} is {nice_size(asize)}, {dest_file} is {nice_size(dsize)}.")

            # If this is a flatfile or monolithic directory, offer to delete older
            if os.path.isfile(abs_f) or dirtype:
                if abs_f_mtime > dest_f_mtime:
                    older_file = dest_file
                else:
                    older_file = abs_f
                del_ok = "f"
                while del_ok == 'f':
                    del_ok = answer(f"Delete older file ({older_file + _dmark(older_file)}) "
                                    "or show diFf [D/n/f]?")
                    if del_ok == 'f':
                        rv = subprocess.run(["diff", "-r", abs_f, dest_file], capture_output=True)
                        print(rv.stdout)
                    if del_ok in ['', 'd', 'y']:
                            remove(older_file)
                            continue
                    if del_ok == 'n':
                        pass
            if os.path.isdir(abs_f):
                abs_f_entries = len(os.listdir(abs_f))
                dest_entries = len(os.listdir(dest_file))
                print(f"{abs_f} holds {abs_f_entries} files, {dest_file} holds {dest_entries}.")

                # Ask for help
                if os.path.isdir(abs_f):
                    action = answer("[C]heck inside, [o]pen in finder, or [s]kip [Cos]?")
                    if action in ["y", "c", ""]:
                        walk(abs_f, dest_file, level + 1)
                    elif action == "o":
                        finderopen(abs_f)
                        finderopen(dest_file)
                    elif action == "s":
                        print("Skipping.")
