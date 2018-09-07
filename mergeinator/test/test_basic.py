import os

from mergeinator import _dmark


def test_dmark_identifies_dirs():
    assert _dmark(".") == "/"


def test_dmark_identifies_plain_files():
    fn = "/tmp/fooby-bletch-xyzzy-666"
    open(fn, "w").close()
    assert _dmark(fn) == ""
    os.remove(fn)
