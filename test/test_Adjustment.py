import sys
sys.path.append('src')
from Adjustment import SplitWorker  # noqa autopep8

worker = SplitWorker()


class TestSplitWorker:
    def test_init(self):
        assert hasattr(worker, 'md')

    def test_get_recent_splits(self):
        df = worker.get_recent_splits(['NVDA', 'TSLA', 'AAPL'], '5y')
        assert len(df) > 0 and len(df) <= 3
