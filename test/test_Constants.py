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

    def test_get_sentiment_path(self):
        assert finder.get_sentiment_path(
            'aapl') == 'data/sentiment/stocktwits/AAPL.csv'
        assert finder.get_sentiment_path(
            'AMD') == 'data/sentiment/stocktwits/AMD.csv'

    def test_get_ohlc_path(self):
        assert finder.get_ohlc_path('aapl') == 'data/ohlc/iexcloud/AAPL.csv'
        assert finder.get_ohlc_path('AMD') == 'data/ohlc/iexcloud/AMD.csv'
