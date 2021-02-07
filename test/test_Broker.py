import os
import sys
import pandas as pd
from datetime import datetime
sys.path.append('src')
from Broker import Robinhood  # noqa autopep8
import Constants as C  # noqa autopep8

rh = Robinhood()
if not C.CI:
    rh.writer.store.bucket_name = os.environ['S3_DEV_BUCKET']
    rh.reader.store.bucket_name = os.environ['S3_DEV_BUCKET']
exp_symbols = ['AAPL', 'FB', 'DIS']


class TestRobinhood:
    def test_init(self):
        assert type(rh).__name__ == 'Robinhood'
        assert hasattr(rh, 'api')
        assert hasattr(rh, 'writer')
        assert hasattr(rh, 'reader')
        assert hasattr(rh, 'finder')

    def test_flatten(self):
        # empty case
        assert rh.flatten([[]]) == []
        # outer list length 1
        assert rh.flatten([[1, 2]]) == [1, 2]
        # outer list length 2
        assert rh.flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

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

        if os.path.exists(symbols_path):
            os.remove(symbols_path)

        rh.save_symbols()
        assert os.path.exists(symbols_path)
        df = rh.reader.load_csv(symbols_path)
        assert 'AAPL' in list(df[C.SYMBOL])

    def get_holdings(self):
        holdings = rh.get_holdings()
        for symbol in exp_symbols:
            assert symbol in holdings
            assert 'name' in holdings[symbol]

    def test_get_symbols(self):
        symbols = set(rh.get_symbols())
        for symbol in exp_symbols:
            assert symbol in symbols
