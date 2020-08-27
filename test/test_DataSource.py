import os
import sys
from time import sleep
from random import choice
import pandas as pd
sys.path.append('src')
from DataSource import MarketData, IEXCloud, Polygon  # noqa autopep8
import Constants as C  # noqa autopep8

md = MarketData()
iex = IEXCloud()
poly = Polygon()
if not os.environ.get('CI'):
    iex.token = os.environ['IEXCLOUD_SANDBOX']
    iex.writer.store.bucket_name = os.environ['S3_DEV_BUCKET']
    iex.reader.store.bucket_name = os.environ['S3_DEV_BUCKET']
    md.writer.store.bucket_name = os.environ['S3_DEV_BUCKET']
    md.reader.store.bucket_name = os.environ['S3_DEV_BUCKET']
    poly.writer.store.bucket_name = os.environ['S3_DEV_BUCKET']
    poly.reader.store.bucket_name = os.environ['S3_DEV_BUCKET']
iex.base = 'https://sandbox.iexapis.com'
iex.base = 'https://sandbox.iexapis.com'
exp_symbols = ['AAPL', 'FB', 'DIS']
retries = 10


class TestMarketData:
    def test_init(self):
        assert type(md).__name__ == 'MarketData'
        assert hasattr(md, 'writer')
        assert hasattr(md, 'reader')
        assert hasattr(md, 'finder')
        assert hasattr(md, 'provider')

    def test_get_symbols(self):
        symbols = set(md.get_symbols())
        for symbol in exp_symbols:
            assert symbol in symbols

    def test_get_dividends(self):
        df = md.get_dividends('AAPL')
        assert {C.EX, C.PAY, C.DEC, C.DIV}.issubset(df.columns)
        assert len(df) > 15
        assert len(df[df[C.EX] < '2015-12-25']) > 0
        assert len(df[df[C.EX] > '2020-01-01']) > 0

    def test_standardize_dividends(self):
        columns = ['exDate', 'paymentDate', 'declaredDate', 'amount']
        new_cols = [C.EX, C.PAY, C.DEC, C.DIV]
        sel_idx = 2
        selected = columns[sel_idx:]
        df = pd.DataFrame({column: [0] for column in columns})
        standardized = md.standardize_dividends('AAPL', df)
        for column in new_cols:
            assert column in standardized

        df.drop(columns=selected, inplace=True)
        standardized = md.standardize_dividends('AAPL', df)
        for curr_idx, column in enumerate(new_cols):
            col_in_df = column in standardized
            assert col_in_df if curr_idx < sel_idx else not col_in_df

    def test_save_dividends(self):
        symbol = 'O'
        div_path = md.finder.get_dividends_path(symbol)
        temp_path = f'{div_path}_TEMP'

        if os.path.exists(div_path):
            os.rename(div_path, temp_path)

        for _ in range(retries):
            iex.save_dividends(symbol=symbol, timeframe='5y')
            if not md.reader.check_file_exists(div_path):
                delay = choice(range(5, 10))
                sleep(delay)
            else:
                break

        assert md.reader.check_file_exists(div_path)
        assert md.reader.store.modified_delta(div_path).total_seconds() < 60
        df = md.reader.load_csv(div_path)
        assert {C.EX, C.PAY, C.DEC, C.DIV}.issubset(df.columns)
        assert len(df) > 0

        if os.path.exists(temp_path):
            os.rename(temp_path, div_path)

    def test_get_splits(self):
        df = md.get_splits('NFLX')
        assert {C.EX, C.DEC, C.RATIO}.issubset(df.columns)
        assert len(df) > 0

    def test_standardize_splits(self):
        columns = ['exDate', 'paymentDate', 'declaredDate', 'ratio']
        new_cols = [C.EX, C.PAY, C.DEC, C.RATIO]
        sel_idx = 2
        selected = columns[sel_idx:]
        df = pd.DataFrame({column: [0] for column in columns})
        standardized = md.standardize_splits('NFLX', df)
        for column in new_cols:
            assert column in standardized

        df.drop(columns=selected, inplace=True)
        standardized = md.standardize_splits('NFLX', df)
        for curr_idx, column in enumerate(new_cols):
            col_in_df = column in standardized
            assert col_in_df if curr_idx < sel_idx else not col_in_df

    def test_save_splits(self):
        pass


class TestIEXCloud:
    def test_init(self):
        assert type(iex).__name__ == 'IEXCloud'
        assert hasattr(iex, 'base')
        assert hasattr(iex, 'version')
        assert hasattr(iex, 'token')
        assert hasattr(iex, 'provider')

    def test_get_endpoint(self):
        parts = [
            iex.base,
            iex.version,
            'stock',
            'aapl',
            'dividend'
            '5y'
        ]
        endpoint = iex.get_endpoint(parts)
        assert len(endpoint.split('/')) == 7
        assert 'token' in endpoint

    def test_get_dividends(self):
        df = []

        for i in range(retries):
            if not len(df):
                df = iex.get_dividends('AAPL', '5y')
                if not i:
                    delay = choice(range(5, 10))
                    sleep(delay)
            else:
                break

        assert len(df) > 0
        assert {C.EX, C.PAY, C.DEC, C.DIV}.issubset(df.columns)

    def test_get_splits(self):
        df1, df2 = [], []
        for i in range(retries):
            if not(len(df1) or len(df2)):
                df1 = iex.get_splits('AAPL', '5y')
                df2 = iex.get_splits('NFLX', '5y')
                if not i:
                    delay = choice(range(5, 10))
                    sleep(delay)
            else:
                break

        assert len(df1) or len(df2)
        assert {C.EX, C.DEC, C.RATIO}.issubset(
            df1.columns) or {C.EX, C.DEC, C.RATIO}.issubset(df2.columns)


class TestPolygon:
    def test_init(self):
        assert type(poly).__name__ == 'Polygon'
        assert hasattr(poly, 'client')
        assert hasattr(poly, 'provider')

    def test_get_dividends(self):
        df = poly.get_dividends('AAPL', '5y')
        assert {C.EX, C.PAY, C.DEC, C.DIV}.issubset(df.columns)
        assert len(df) > 0

    def test_get_splits(self):
        df = poly.get_splits('AAPL')
        assert {C.EX, C.DEC, C.RATIO}.issubset(df.columns)
        assert len(df) > 0
