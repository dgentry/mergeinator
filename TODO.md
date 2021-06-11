## Possible Improvements

See NEWS for fixed items from this list

* Make merge a replacement for mv:
  ** If there are a bunch of args, merge them all into the last one

* When the source file doesn't end in / and the destination does,
  append the basename of the source to the destination, e.g.:
    merge foo a/
  means merge foo a/foo.  I think this is what mv, diff, etc., do.


* Generate merge plan and then execute it
Ideally, merging would work by generating a merge plan for the entire
pair of directories, then carrying it out in one pass.  That might be
easiest with a fresh rewrite.  (It currently requires multiple passes.
For directory trees that are only similar, but not identical, each
pass may only merge one layer of directory hierarchy; so to fully
merge and eliminate the source directory, you may have to run it as
many times as the depth of your hierarchy.)

* There are 10 tests
It's only lightly tested (either in real-world usage, where it has
helped me clean up several longstanding near-duplicate directory trees
and clear off a Time Machine Backup disk) or in unit- or integration
tests (there are two small unit tests).

* A Mac UI might be helpful to non-command-line users.

* Visualizing which file differs and which one is newer/older/larger
might help the user choose better/quicker.

* For older/newer differing files, it could offer more ways to figure
out which one you want and/or merge them.

* Logging could be yet more readable. (how?)

* When merging an empty source directory, (offer to?) delete it.  (This
would be the last pass if you have made multiple runs.)

* Lazy Diff
It should do a lazy diff.  [It counts files in directories, at least].
It currently relies on gnu diffutils (there is a deficiency in macOS
diff), and as soon as we find any difference, we don't need to
continue finding additional diffs or details thereof.  Perhaps
gnudiff's `-q`/`-brief` flag causes it to be lazy?  The quickest check
I can think of would be file size.  Once one pair of files differ in
length, that pair, and any pair of parent directory trees, definitely
differ.

* Safer --yes flag
There could be a quicker, yet safe flag, perhaps `--safe-yes`.  The
`-y` flag is slightly berzerk in that it arbitrarily chooses to delete
the older versions of files that differ.  `--Safe-yes` should only
delete identical files (not older ones that differ).

* The quick answer choices could have clearer one-letter
answers/defaults.

* One could fix the weird situations in which it crashes (see Issue
Tracker), for example, when files are deleted out from under it when
running.

* This list of improvements could go in the github Issue Tracker.
