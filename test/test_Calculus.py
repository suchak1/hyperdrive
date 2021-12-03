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
        smoothed = calc.smooth(series)
        expected = [-8, 36, 63, 79, 63, 36, -8]
        for idx, s in enumerate(smoothed):
            assert round(s) == expected[idx]

    def test_derive(self):
        pass

    def test_cv(self):
        pass
