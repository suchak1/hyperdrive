import sys
sys.path.append('src')
from Adjustment import SplitWorker  # noqa autopep8

worker = SplitWorker()


class TestSplitWorker:
    def test_init(self):
        assert hasattr(worker, 'md')
