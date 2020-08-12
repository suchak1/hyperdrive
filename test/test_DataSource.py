import os
import sys
from time import sleep
from random import choice
sys.path.append('src')
from DataSource import MarketData, IEXCloud  # noqa autopep8
import Constants as C  # noqa autopep8

md = MarketData()
iex = IEXCloud()
if not os.environ.get('CI'):
    iex.token = os.environ['IEXCLOUD_SANDBOX']
iex.base = 'https://sandbox.iexapis.com'
exp_symbols = ['AAPL', 'FB', 'DIS']


class TestMarketData:
    def test_init(self):
        assert type(md).__name__ == 'MarketData'
        assert hasattr(md, 'writer')
        assert hasattr(md, 'reader')
        assert hasattr(md, 'finder')

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

    def test_save_dividends(self):
        symbol = 'O'
        div_path = md.finder.get_dividends_path(symbol)
        test_path = f'{div_path}_TEST'
        if not os.path.exists(div_path):
            md.writer.store.download_file(div_path)
        md.writer.rename_file(div_path, test_path)
        assert not md.reader.check_file_exists(div_path)

        retries = 10
        delay = choice(range(5, 10))
        for _ in range(retries):
            iex.save_dividends(symbol, '5y')
            if not md.reader.check_file_exists(div_path):
                sleep(delay)
            else:
                break

        assert md.reader.check_file_exists(div_path)
        md.writer.remove_files([div_path])
        md.writer.rename_file(test_path, div_path)


class TestIEXCloud:
    def test_init(self):
        assert type(iex).__name__ == 'IEXCloud'
        assert hasattr(iex, 'base')
        assert hasattr(iex, 'version')
        assert hasattr(iex, 'token')

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
        df = iex.get_dividends('AAPL', '5y')
        assert type(df).__name__ == 'DataFrame'

        if len(df) > 0:
            assert {C.EX, C.PAY, C.DEC, C.DIV}.issubset(df.columns)
