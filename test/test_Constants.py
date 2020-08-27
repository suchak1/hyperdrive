import sys
sys.path.append('src')
from Constants import PathFinder  # noqa autopep8


finder = PathFinder()


class TestPathFinder():
    def test_init(self):
        assert type(PathFinder()).__name__ == 'PathFinder'

    def test_get_symbols_path(self):
        assert finder.get_symbols_path() == 'data/symbols.csv'

    def test_get_dividends_path(self):
        assert finder.get_dividends_path(
            'aapl') == 'data/dividends/iexcloud/AAPL.csv'
        assert finder.get_dividends_path(
            'AMD') == 'data/dividends/iexcloud/AMD.csv'

    def test_get_splits_path(self):
        assert finder.get_splits_path(
            'aapl') == 'data/splits/iexcloud/AAPL.csv'
        assert finder.get_splits_path(
            'AMD') == 'data/splits/iexcloud/AMD.csv'
