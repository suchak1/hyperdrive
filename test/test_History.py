import sys
sys.path.append('src')
from History import Historian  # noqa autopep8


hist = Historian()


class TestHistorian:
    def test_buy_and_hold(self):
        stats = hist.buy_and_hold('X%3ABTCUSD', '1y')
        assert 'Sortino Ratio' in stats
