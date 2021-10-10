import sys
import numpy as np
sys.path.append('src')
from History import Historian  # noqa autopep8


hist = Historian()
ls = [np.nan, True, True, np.nan, False, np.nan, np.nan, np.nan, True]
fs = [True,   True, True, True,   False, False,  False,  False,  True]
ns = [True,   True, True, True,   False, False,  False,  True,   True]
arr = np.array(ls)
test_ffill = np.array(fs)
test_nfill = np.array(ns)


close = np.array([3, 2, 5, 1, 100, 75, 50, 25, 1])


class TestHistorian:
    def test_buy_and_hold(self):
        stats = hist.buy_and_hold('X%3ABTCUSD', '1y').stats()
        assert 'Sortino Ratio' in stats

    def test_create_portfolio(self):
        stats = hist.create_portfolio(close, test_ffill).stats()
        assert 'Sortino Ratio' in stats

    def test_fill(self):
        ffill = hist.fill(arr)
        assert np.array_equal(ffill, test_ffill)
        nfill = hist.fill(arr, 'nearest')
        assert np.array_equal(nfill, test_nfill)

    def test_get_optimal_signals(self):
        f_signals = hist.get_optimal_signals(close, n=2, method='ffill')
        assert np.array_equal(f_signals, test_ffill)
        n_signals = hist.get_optimal_signals(close, n=2, method='nfill')
        assert np.array_equal(n_signals, test_nfill)

    def test_generate_random(self):
        strats = hist.generate_random(close, num=10)
        assert sum(strats) > 0 and len(strats)
