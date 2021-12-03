
import numpy as np
from scipy.signal import savgol_filter


class Calculator:
    def delta(self, series):
        return series / series.shift() - 1

    def roll(self, series, window):
        return series.rolling(window).mean()

    def smooth(self, series, window, order):
        return savgol_filter(
            series,
            window + 1 if window % 2 == 0 else window + 2,
            order
        )

    def derive(y, x):
        x_delta = (
            x.values.astype('float64')[1] -
            x.values.astype('float64')[0]
        )
        return np.gradient(y, x_delta)

    def cv(self, df, axis):
        return df.std(axis=axis) / df.mean(axis=axis)

    def fib(self, n, accumulator=0):
        if n <= 1:
            return 0
        elif n == 2:
            return 1
        else:
            return (
                self.fib(n - 1, accumulator) +
                self.fib(n - 2, accumulator)
            )
