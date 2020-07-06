import os
import sys
import pandas as pd
from datetime import datetime
sys.path.append('src')
from scarlett import \
    flatten, save_json, load_json, save_csv, load_csv, Scarlett  # noqa autopep8

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_flatten():
    # empty case
    assert flatten([[]]) == []
    # outer list length 1
    assert flatten([[1, 2]]) == [1, 2]
    # outer list length 2
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


json_path1 = os.path.join(dir_path, 'test1.json')
json_path2 = os.path.join(dir_path, 'test2.json')

empty = {}
data = [
    {
        'symbol': 'AMZN',
        'open': 2400.85,
        'volume': 402265
    },
    {
        'symbol': 'AAPL',
        'open': 300.90,
        'volume': 502265

    }
]


def test_save_json():
    # save empty json object
    save_json(json_path1, {})
    assert os.path.exists(json_path1)

    # save list of 2 json objects
    save_json(json_path2, data)
    assert os.path.exists(json_path2)


def test_load_json():
    # empty case from above
    assert load_json(json_path1) == empty
    # mock data case from above
    assert load_json(json_path2) == data


csv_path1 = os.path.join(dir_path, 'test1.csv')
csv_path2 = os.path.join(dir_path, 'test2.csv')
test_df = pd.DataFrame(data)
empty_df = pd.DataFrame()


def test_save_csv():
    # save empty table
    save_csv(csv_path1, empty_df)
    assert os.path.exists(csv_path1)

    # save table with 2 rows
    save_csv(csv_path2, test_df)
    assert os.path.exists(csv_path2)


def test_load_csv():
    # empty case from above
    assert load_csv(csv_path1).equals(empty_df)
    # mock data case from above
    assert load_csv(csv_path2).equals(test_df)


sl = Scarlett()


def test_init():
    assert hasattr(sl, 'rh') is True


def test_load_portfolio():
    sl.load_portfolio()
    assert hasattr(sl, 'positions') is True
    assert hasattr(sl, 'holdings') is True
    assert hasattr(sl, 'instruments') is True
    assert hasattr(sl, 'symbols') is True
    assert hasattr(sl, 'hist') is True


exp_symbols = ['AAPL', 'FB', 'DIS']


def test_get_symbols():
    instruments = list(sl.instruments)
    symbols = set(sl.get_symbols(instruments))
    for symbol in exp_symbols:
        assert symbol in symbols


def test_get_hists():
    df = sl.get_hists(exp_symbols)
    curr_year = datetime.today().year - 3
    ts = pd.Timestamp(curr_year, 1, 1, 12)

    for symbol in exp_symbols:
        assert len(df[df['symbol'] == symbol]) > 100
        assert len(df[df['begins_at'] < ts]) > 0
