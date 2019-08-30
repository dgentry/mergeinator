## What it does
The mergeinator merges a directory (the "source directory") into a similar directory
(the "destination," which can be a parent of the source directory), eliminating
duplicates as it goes.  After several runs, the source directory should be gone,
merged into the destination.

## How to run it
```
$ merge old_home_dir_copy ~/
```

The `-y` or `--yes` flag causes it to "auto answer" interactive questions with "yes."  If
you use this, there are cases where you could lose info (conflicting changes in files -- it
chooses the newer one, when there could be useful changes in the old file as well).

The `-n` or `--dryrun` flag causes `merge` to print the actions it would take, but not
actually change any files.

## Why would you want this?
Every time I make a tarball of my directory tree, I later end up expanding it somewhere
within my directory tree, so I end up with a mostly older copy of my main tree embedded in
my real tree.  Cleaning it up is a pain because if you just delete the whole thing, you
might lose some stuff you want.  Merging stuff you might want manually first is error-prone
and takes forever.

## Better than alternatives
It's better for this purpose than the commercial de-dup utilities I've found because it
works on higher-level units first, rather than, e.g., reporting that you have a dozen
identical empty .DS_Store files.

For example, if the destination has a Projects directory with 10 projects, but there is a
single missing one that's only in the source directory, merge will move the one missing
project in its entirety from the source to the destination's Projects directory (and delete
the duplicate projects from the source as well).

## Possible Improvements
It's a little more work, though.  For directory trees that are only similar, but not
identical, each pass may only merge one layer of directory hierarchy; so to fully merge and
eliminate the source directory, you may have to run it as many times as the depth of your
hierarchy.

It's also not particularly well tested (either in real-world usage, where it has helped me
clean up several longstanding near-duplicate directory trees) or in unit- or integration
tests (there are two small unit tests).

Maybe someday I'll put a Mac UI on it.

Visualizing which file differs and which one is newer/older/larger
might help the user choose better/quicker.

Maybe file on left is always white, file on right is always yellow or
something like that.  (On black background)

Better Logging

When merging empty directory, (offer to) delete source dir


## To install
```
make install
```

If there is interest, I'll put it on pypi.

## Developer Notes
Packaged according to this scheme, which seems extremely sensible:
https://blog.ionelmc.ro/2014/05/25/python-packaging
