import os
import sys
import pandas as pd
from datetime import datetime
sys.path.append('src')
from Broker import Robinhood  # noqa autopep8

rh = Robinhood()
exp_symbols = ['AAPL', 'FB', 'DIS']


class TestRobinhood:
    def test_init(self):
        assert type(rh).__name__ == 'Robinhood'
        assert hasattr(rh, 'api')

    def test_flatten(self):
        # empty case
        assert rh.flatten([[]]) == []
        # outer list length 1
        assert rh.flatten([[1, 2]]) == [1, 2]
        # outer list length 2
        assert rh.flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_load_portfolio(self):
        rh.load_portfolio()
        assert hasattr(rh, 'positions')
        assert hasattr(rh, 'holdings')
        assert hasattr(rh, 'instruments')
        assert hasattr(rh, 'symbols')
        assert hasattr(rh, 'hist')

    def test_get_symbols_from_instruments(self):
        instruments = list(rh.instruments)
        symbols = set(rh.get_symbols_from_instruments(instruments))
        for symbol in exp_symbols:
            assert symbol in symbols

    def test_get_hists(self):
        df = rh.get_hists(exp_symbols, span='5year', interval='week')
        curr_year = datetime.today().year - 3
        ts = pd.Timestamp(curr_year, 1, 1, 12)

        for symbol in exp_symbols:
            assert len(df[df['symbol'] == symbol]) > 100
            assert len(df[df['begins_at'] < ts]) > 0

    def test_get_names(self):
        assert rh.get_names([]) == []
        assert rh.get_names(exp_symbols) == ['Apple', 'Facebook', 'Disney']

    def test_save_symbols(self):
        symbols_path = rh.finder.get_symbols_path()
        test_path = f'{symbols_path}_TEST'
        os.rename(symbols_path, test_path)
        assert not os.path.exists(symbols_path)
        rh.save_symbols()
        assert os.path.exists(symbols_path)
        os.remove(symbols_path)
        os.rename(test_path, symbols_path)
