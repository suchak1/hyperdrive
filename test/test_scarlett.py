import sys
import pytest_check as check
sys.path.append('src')
from scarlett import *  # nopep8


def test_flatten():
    # empty case
    check.equal(flatten([[]]), [])

    check.equal(flatten([[1, 2]]), [1, 2])

    check.equal(flatten([[1, 2], [3, 4]]), [1, 2, 3, 4])
