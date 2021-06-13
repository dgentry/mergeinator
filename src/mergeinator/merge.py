#!/usr/bin/env python3
"""CLI wrapper for mergeinator()"""

from click import command, argument, option, version_option, echo, Path
import pkg_resources  # For version number
from os.path import abspath, exists, isfile, isdir, basename
from sys import exit

from mergeinator import WHT, NORMAL, do_merge, move_maybe


@command()
@argument("source", type=Path())
@argument("destination", type=Path())
@option("-n", "--dryrun", help="Don't change anything", is_flag=True)
@option("-y", "--yes", help="force answer of yes to questions.", is_flag=True)
@version_option()
def cli(source, destination, dryrun, yes):
    """Merge helps get rid of duplicate files and directory trees.

    If source and destination are both files, and the destination file
    has the same content as the source file, merge will delete the
    source file.  If the content differs, it will offer to move the
    source to the same directory as the destination with a unique name.

    If the destination is a directory, it will move the source file to
    that directory, unless there is an identically named file in the
    destination, in which case it will act as above (delete if dup,
    offer move with unique name if not).

    If the source and destination are both directories, it will trim
    away the source directory by moving its unique content into the
    destination directory.  Duplicate content is discarded.  It may
    require multiple runs of merge (one per level of subdirectory
    depth) to completely remove all duplicate content because merge
    won't remove non-empty directories, and duplicate directories
    don't become empty until after they are merged.

    If the source is a directory and the destination is a file, you're
    holding it wrong.
    """
    my_version = pkg_resources.require("mergeinator")[0].version
    echo(f"Mergeinator {my_version}")
    if not exists(source):
        echo(f"{WHT}{source}{NORMAL} doesn't exist.  My work here is done.")
        exit(0)
    echo(f"Merging {WHT}{source}{NORMAL} to {WHT}{destination}{NORMAL}\n")
    echo(f"Full paths: {abspath(source)} to {abspath(destination)}\n")
    if isfile(source) and isfile(destination):
        move_maybe(source, destination, yes_flag=yes, dry_run_flag=dryrun)
    elif isfile(source) and isdir(destination):
        move_maybe(source, destination + basename(source), yes_flag=yes, dry_run_flag=dryrun)
    elif isdir(source) and isdir(destination):
        do_merge(source, destination, 0, yes_flag=yes, dry_run_flag=dryrun)
    else:
        echo(f"I'm not prepared for whatever {source} and {destination} are.")
