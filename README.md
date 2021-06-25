## What it does
Clean up your files and recover disk space with The Merginator.

The Mergeinator efficiently merges a directory tree (the "source")
into a similar directory tree (the "destination"), eliminating
duplicates from the source directory as it goes.  After several runs,
the source directory is gone, merged into the destination.  (It works
even when the source directory is inside the destination, which is
useful when you've expanded a tarball of your home directory within
it.)

It also deals with permission settings that would otherwise prevent
you from moving/deleting duplicate files, especially on MacOS, which
has many ways to lock files, especially if they are part of a Time
Machine backup.

It works best on MacOS, but should mostly work on any Unix/Linux/Posix
system.  If anyone is interested, I'll separate out the MacOS-specific
stuff that lets it deal with Time Machine Backups.


## How to run it
```
$ merge old_home_dir_copy ~/
```
I run it "manually" (as above) and answer the questions it
asks a few times.  This lets me confirm that it's doing what I
intended.  When I get tired of answering questions, I re-run it with
the `-y` flag and let 'er rip.

The `-y` or `--yes` flag causes it to "auto answer" questions with
"yes."  It is possible to lose info with this flag.  When there are
conflicting changes in files, it arbitrarily chooses the newer one,
when there could be useful changes in the old file as well.

If you are cautious, your first run could be with the `-n` or
`--dryrun` flag, which causes `merge` to print the actions it would
take, but not actually change any files.

Without any flags, `merge` will only make "safe" (i.e., reversible)
changes without asking.  For example, when two files are identical, it
will delete the source version, which you could (perhaps
painstakingly) restore with a `cp <dest> <source>` if you later
decided it was a mistake.  All operations are logged in `merge.log`.


## Why would you want this?

Everyone ends up with duplicate files or directory trees sometimes,
which clutter up your hierarchy and possibly double or triple the
storage space you need.

In particular, every time I make a tarball of (a part of) my directory
tree for safekeeping, I later end up expanding it somewhere within my
directory tree, so I end up with a mostly older copy of my main tree
embedded in my current tree.  Cleaning it up is a pain because if you
just delete the whole thing, you might lose some stuff you want.
Manually looking for and saving that stuff (with, say, `diff -r` and
then `mv`) is error-prone and takes forever.  [Perhaps the real lesson
is don't make these dumb safekeeping tarballs in the first place, but
somehow I've always ended up with one when I've moved from one primary
computer to another.  I am now better at using `git` correctly in the
first place too.]

It also seems to work when merging two similar iPhoto or iTunes
libraries, although iPhoto needs a re-index afterwards.  (Probably
iTunes also needs some kind of re-index but I haven't noticed that.)


## Better than alternatives
It's better for de-duping your stuff than the commercial de-dup
utilities I've found because it works on higher-level units (say,
entire directory trees) first, rather than, e.g., reporting that you
have a dozen identical empty `.DS_Store` files, which isn't that
helpful.

For example, if the destination has a Projects directory with 10
projects, but there is a single missing one that's only in the source
directory, merge will move exactly the one missing project in its
entirety from the source to the destination's Projects directory (and
delete the duplicate projects from the source as well), leaving your
destination directory complete and organized.


## To install

You'll need Python 3.6 or newer, and gnudiff (typically the default on
most Linux distros, but not MacOS).

On Mac, install Python 3 and GNU diff.
```
brew install python3 gnudiff
```

Fetch the repo and build:
```
git clone https://github.com/dgentry/mergeinator
cd mergeinator
make install
```

If there is interest, I'll put it on pypi.



## Developer Notes
Packaged according to this scheme, which seems extremely sensible:
https://blog.ionelmc.ro/2014/05/25/python-packaging
