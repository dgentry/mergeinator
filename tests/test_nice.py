import os

from mergeinator import nice_size, nicedelta


def test_nice_size_MB():
    assert nice_size(1_048_576)=="1.0 MB"

    assert nice_size(1_110_432)=="1.06 MB"
