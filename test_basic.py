import os

from merge_up import dmark


def test_dmark_identifies_dirs():
    assert dmark(".") == "/"


def test_dmark_identifies_plain_files():
    fn = "/tmp/fooby-bletch-xyzzy-666"
    open(fn, "w").close()
    assert dmark(fn) == ""
    os.remove(fn)
