import os
import sys
sys.path.append('src')
from DataSource import MarketData, IEXCloud  # noqa autopep8
import Constants as C  # noqa autopep8

md = MarketData()
iex = IEXCloud()
exp_symbols = ['AAPL', 'FB', 'DIS']
exp_symbol = 'AAPL'


class TestMarketData:
    def test_init(self):
        assert hasattr(md, 'writer')
        assert hasattr(md, 'reader')
        assert hasattr(md, 'finder')

    def test_get_symbols(self):
        symbols = set(md.get_symbols())
        for symbol in exp_symbols:
            assert symbol in symbols

    def test_get_dividends(self):
        df = md.get_dividends(exp_symbol)
        assert {C.EX, C.PAY, C.DEC, C.DIV}.issubset(df.columns)
        assert len(df) > 15
        assert len(df[df[C.EX] < '2015-12-25']) > 0
        assert len(df[df[C.EX] > '2020-01-01']) > 0

    def test_save_dividends(self):
        md.save_dividends(exp_symbol)
        assert os.path.exists(
            md.finder.get_dividends_path(exp_symbol)
        )


class TestIEXCloud:
    def test_init(self):
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
        pass
