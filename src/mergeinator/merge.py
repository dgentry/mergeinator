#!/usr/bin/env python3
"""CLI wrapper for mergeinator()"""

from click import command, argument, option, version_option, echo, Path
import pkg_resources  # For version number
from os.path import abspath
from mergeinator import WHT, NORMAL, DIM, do_merge


@command()
@argument("source", type=Path(exists=True))
@argument("destination", type=Path(exists=True))
@option("-n", "--dryrun", help="Don't change anything", is_flag=True)
@option("-y", "--yes", help="force answer of yes to questions.", is_flag=True)
@version_option()
def cli(source, destination, dryrun, yes):
    """Merge trims away the source directory by moving its unique content into the destination
    directory.  Duplicate content is discarded.  It may take multiple runs of merge (one per
    level of subdirectory depth) to completely remove all duplicate content because merge
    won't remove non-empty directories, and duplicate directories don't become empty until
    after they are merged.
    """
    my_version = pkg_resources.require("mergeinator")[0].version
    echo(f"Mergeinator {my_version}")
    echo(f"Merging {WHT}{source}{NORMAL} to {WHT}{destination}{NORMAL}\n")
    echo(f"Full paths: {abspath(source)} to {abspath(destination)}\n")
    do_merge(source, destination, 0, yes_flag=yes, dry_run_flag=dryrun)
