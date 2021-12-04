import sys
import numpy as np
import pandas as pd
sys.path.append('hyperdrive')
from Calculus import Calculator  # noqa autopep8

calc = Calculator()


class TestCalculator:
    def test_delta(self):
        series = pd.Series([50, 100, 25])
        shifted = calc.delta(series)
        expected = pd.Series([np.nan, 1, -0.75])
        assert shifted.equals(expected)

    def test_roll(self):
        series = pd.Series([1, 2, 3])
        rolled = calc.roll(series, 2)
        expected = pd.Series([np.nan, 1.5, 2.5])
        assert rolled.equals(expected)

    def test_smooth(self):
        series = pd.Series([0, 25, 50, 100, 50, 25, 0])
        smoothed = calc.smooth(series, 3, 2)
        expected = [-8, 36, 63, 79, 63, 36, -8]
        for idx, s in enumerate(smoothed):
            assert round(s) == expected[idx]

    def test_derive(self):
        series = pd.Series(calc.fib(9))
        derived = calc.derive(series)
        expected = pd.Series([1, 0.5, 0.5, 1, 1.5, 2.5, 4, 6.5, 8])
        assert np.array_equal(derived, expected)

    def test_cv(self):
        series = pd.Series([2, 4, 6])
        cvd = calc.cv(series)
        expected = 0.5
        assert cvd == expected

    def test_fib(self):
        assert calc.fib(9) == [0, 1, 1, 2, 3, 5, 8, 13, 21]
