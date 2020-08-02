import sys
import pandas as pd
from datetime import datetime
sys.path.append('src')
from Algotrader import Scarlett  # noqa autopep8

sl = Scarlett()
exp_symbols = ['AAPL', 'FB', 'DIS']


class TestScarlett:
    def test_init(self):
        assert hasattr(sl, 'api') is True

    def test_flatten(self):
        # empty case
        assert sl.flatten([[]]) == []
        # outer list length 1
        assert sl.flatten([[1, 2]]) == [1, 2]
        # outer list length 2
        assert sl.flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_load_portfolio(self):
        sl.load_portfolio()
        assert hasattr(sl, 'positions') is True
        assert hasattr(sl, 'holdings') is True
        assert hasattr(sl, 'instruments') is True
        assert hasattr(sl, 'symbols') is True
        assert hasattr(sl, 'hist') is True

    def test_get_symbols_from_instruments(self):
        instruments = list(sl.instruments)
        symbols = set(sl.get_symbols_from_instruments(instruments))
        for symbol in exp_symbols:
            assert symbol in symbols

    def test_get_hists(self):
        df = sl.get_hists(exp_symbols, span='5year', interval='week')
        curr_year = datetime.today().year - 3
        ts = pd.Timestamp(curr_year, 1, 1, 12)

        for symbol in exp_symbols:
            assert len(df[df['symbol'] == symbol]) > 100
            assert len(df[df['begins_at'] < ts]) > 0
