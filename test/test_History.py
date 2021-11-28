import sys
import numpy as np
import pandas as pd
sys.path.append('hyperdrive')
from History import Historian  # noqa autopep8


hist = Historian()
ls = [np.nan, True, True, np.nan, False, np.nan, np.nan, np.nan, True]
fs = [True,   True, True, True,   False, False,  False,  False,  True]
unfilled_fs = [True, None, None, None,
               False, None, None, None, True]
ns = [True,   True, True, True,   False, False,  False,  True,   True]
unfilled_ns = [True, None, None, None,
               False, None, None, True, True]
arr = np.array(ls)
test_ffill = np.array(fs)
test_nfill = np.array(ns)


close = np.array([3, 2, 5, 1, 100, 75, 50, 25, 1])

total = 100
majority = 80
minority = total - majority
data = np.arange(total)
X = pd.DataFrame({'i': data, 'j': data})
y = np.array([True] * majority + [False] * minority)


class TestHistorian:
    def test_buy_and_hold(self):
        stats = hist.buy_and_hold(close).stats()
        assert 'Sortino Ratio' in stats

    def test_create_portfolio(self):
        stats = hist.create_portfolio(close, test_ffill).stats()
        assert 'Sortino Ratio' in stats

    def test_fill(self):
        ffill = hist.fill(arr)
        assert np.array_equal(ffill, test_ffill)
        nfill = hist.fill(arr, 'nearest')
        assert np.array_equal(nfill, test_nfill)

    def test_unfill(self):
        hist.unfill(fs) == unfilled_fs
        hist.unfill(ns) == unfilled_ns

    def test_get_optimal_signals(self):
        f_signals = hist.get_optimal_signals(close, n=2, method='ffill')
        assert np.array_equal(f_signals, test_ffill)
        n_signals = hist.get_optimal_signals(close, n=2, method='nfill')
        assert np.array_equal(n_signals, test_nfill)

    def test_generate_random(self):
        strats = hist.generate_random(close, num=100)
        assert 0 < len(strats) <= 25

    def test_undersample(self):
        y_train = hist.undersample(X, y)[2]
        assert np.mean(y_train) == 0.5

    def test_run_classifiers(self):
        X_train, X_test, y_train, y_test = hist.undersample(X, y)[:4]
        clfs = hist.run_classifiers(X_train, X_test, y_train, y_test)
        for _, clf in clfs:
            assert 'score' in clf
