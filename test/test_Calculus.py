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
