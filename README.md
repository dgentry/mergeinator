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


## Possible Improvements
Ideally, merging would work by generating a merge plan for the entire
pair of directories, then carrying it out in one pass.  That might be
easiest with a fresh rewrite.  (It currently requires multiple passes.
For directory trees that are only similar, but not identical, each
pass may only merge one layer of directory hierarchy; so to fully
merge and eliminate the source directory, you may have to run it as
many times as the depth of your hierarchy.)

It's only lightly tested (either in real-world usage, where it has
helped me clean up several longstanding near-duplicate directory trees
and clear off a Time Machine Backup disk) or in unit- or integration
tests (there are two small unit tests).

Someday a Mac UI might be helpful to non-command-line users.

Visualizing which file differs and which one is newer/older/larger
might help the user choose better/quicker.

Maybe the ASCII UI could have the file on left be always white, file
on right always yellow or something like that.  (On black background)

Logging could be yet more readable.

When merging an empty source directory, (offer to?) delete it.  (This
would be the last pass if you have made multiple runs.)

It should do a lazy diff.  It currently relies on gnu diffutils (there
is a deficiency in macOS diff), and as soon as we find any
difference, we don't need to continue finding additional diffs or
details thereof.  Perhaps gnudiff's `-q`/`-brief` flag causes it to be
lazy?  The quickest check I can think of would be file size.  Once one
pair of files differ in length, that pair, and any pair of parent
directory trees, definitely differ.

There could be a quicker, yet safe flag, perhaps `--safe-yes`.  The
`-y` flag is slightly berzerk in that it arbitrarily chooses to delete
the older versions of files that differ.  `--Safe-yes` should only
delete identical files (not older ones that differ).

For older/newer differing files, it could offer more ways to figure
out which one you want and/or merge them.

The quick answer choices could have clearer one-letter
answers/defaults.

One could fix the weird situations in which it crashes (see Issue
Tracker), for example, when files are deleted out from under it when
running.

This list of improvements could go in the github Issue Tracker.


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
