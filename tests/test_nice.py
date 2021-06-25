import os

from mergeinator import nice_size, nicedelta

def test_nice_size():
    assert nice_size(1_048_576)=="1.0 MB"

    assert nice_size(1_110_432)=="1.06 MB"


def test_nicedelta():
    delta = 365 * 5 * 24 * 60 * 60 + 4000
    assert nicedelta(delta) == "5Y 1h "

    delta = 99999999
    assert nicedelta(delta) == "3Y 2M "

    delta = 0.01
    assert nicedelta(delta) == "10ms "
