#!/usr/bin/env python3

import click
from click import echo
import os
import mergeinator
from mergeinator import WHT, NORMAL


@click.command()
@click.argument("source", required=True)
@click.argument("destination", required=True)
@click.option("-n", "--dryrun", help="Don't change anything", is_flag=True)
@click.option("-y", "--yes", help="force answer of yes to questions.", is_flag=True)
def cli(source, destination, dryrun, yes):
    """Merge trims away the source directory by moving its unique content into the destination
    directory.  Duplicate content is discarded.
    """
    echo(f"Merging {WHT}{source}{NORMAL} ({os.path.abspath(source)}) to "
         f"{WHT}{destination}{NORMAL} ({os.path.abspath(destination)})\n")
    mergeinator.do_merge(source, destination, 0, yes_flag=yes, dry_run_flag=dryrun)
