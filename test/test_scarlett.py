import sys
sys.path.append('src')
from scarlett import *  # nopep8


def test_flatten():
    # empty case
    assert flatten([[]]) == []
    # outer list length 1
    assert flatten([[1, 2]]) == [1, 2]
    # outer list length 2
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]
