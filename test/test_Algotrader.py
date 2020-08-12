import sys
sys.path.append('src')
from Algotrader import Scarlett  # noqa autopep8


sl = Scarlett()


class TestScarlett:
    def test_init(self):
        assert type(sl).__name__ == 'Scarlett'
        assert hasattr(sl, 'broker')
