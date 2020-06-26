import os
import sys
sys.path.append('src')
from scarlett import \
    flatten, save_file, load_file, Scarlett  # noqa autopep8

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_flatten():
    # empty case
    assert flatten([[]]) == []
    # outer list length 1
    assert flatten([[1, 2]]) == [1, 2]
    # outer list length 2
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


file_path1 = os.path.join(dir_path, 'test1.json')
file_path2 = os.path.join(dir_path, 'test2.json')

empty = {}
data = [
    {
        'symbol': 'AMZN',
        'open': '2400.00',
        'volume': 402265
    },
    {
        'symbol': 'AAPL',
        'open': '300.00',
        'volume': 502265

    }
]


def test_save_file():
    # save empty json object
    save_file(file_path1, {})
    assert os.path.exists(file_path1)

    # save list of 2 json objects
    save_file(file_path2, data)
    assert os.path.exists(file_path2)


def test_load_file():
    # empty case from above
    assert load_file(file_path1) == empty
    # mock data case from above
    assert load_file(file_path2) == data


sl = Scarlett()


def test_init():
    assert hasattr(sl, 'rh') == True


def test_get_symbols():


def test_get_hists():


def test_load_portfolio():
    sl.load_portfolio()
    assert hasattr(sl, 'positions') == True
    assert hasattr(sl, 'holdings') == True
    assert hasattr(sl, 'instruments') == True
    assert hasattr(sl, 'symbols') == True
    assert hasattr(sl, 'hist') == True
