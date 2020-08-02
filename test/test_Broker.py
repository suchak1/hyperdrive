import sys
import pandas as pd
from datetime import datetime
sys.path.append('src')
from Algotrader import \
    flatten, save_json, load_json, save_csv, load_csv, Scarlett  # noqa autopep8

# sl = Scarlett(load=True)


def test_flatten():
    # empty case
    assert flatten([[]]) == []
    # outer list length 1
    assert flatten([[1, 2]]) == [1, 2]
    # outer list length 2
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_init():
    assert hasattr(sl, 'rh') is True


def test_load_portfolio():
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
    df = sl.get_hists(exp_symbols, span='5year', interval='week')
    curr_year = datetime.today().year - 3
    ts = pd.Timestamp(curr_year, 1, 1, 12)

    for symbol in exp_symbols:
        assert len(df[df['symbol'] == symbol]) > 100
        assert len(df[df['begins_at'] < ts]) > 0
