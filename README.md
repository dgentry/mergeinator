## What it does

The mergeinator merges a directory (the "source directory) into a similar directory (the
"destination" which doesn't have to be a parent of the source directory), eliminating
duplicates as it goes.  After several runs, the source directory should be gone, merged into
the destination.

## How to run it
```
$ merge old_home_dir_copy ~/
```

## Why would you want this?

Every time I make a tarball of my directory tree, I later end up expanding it somewhere
within my (future) directory tree, so I end up with a mostly older copy of my main tree.

## Better than alternatives
It's better for this purpose than the commercial de-dup utilities I've found because it
works on higher-level units first, rather than reporting that you have a dozen identical
empty .DS_Store files.

For example, if the destination has a Projects directory with 10 projects, but there is a
single missing one that's only in the source directory, merge will move the entire missing
project from the source to the destination's Projects directory (and delete the duplicate
projects from the source as well).

## Possible Improvements
It's a little more work, though.  For directory trees that are only similar, but not
identical, each pass may only merge one layer of directory hierarchy; so to fully merge and
eliminate the source directory, you may have to run it as many times as the depth of your
hierarchy.

It's also not particularly well tested (either in real-world usage, where it has helped me
clean up several longstanding near-duplicate directory trees) or in unit- or integration
tests (there are two small unit tests).

Maybe someday I'll put a Mac UI on it.

## To install
```
make install
```
