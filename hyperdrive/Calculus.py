
import numpy as np
import pandas as pd
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

    def derive(self, y, x=np.array([0, 1])):
        if type(x) == pd.Series:
            x = x.to_numpy()
        x = x.astype('float64')
        x_delta = (x[1] - x[0])
        return np.gradient(y, x_delta)

    def cv(self, x):
        if type(x) == pd.Series:
            axis = 0
        else:
            axis = 1
        # consider supporting ddof=0 and rebuilding model
        return x.std(axis=axis) / x.mean(axis=axis)

    def fib(self, n):
        if n <= 1:
            return [0]
        elif n == 2:
            return [0, 1]
        else:
            lst = self.fib(n - 1)
            return self.fib(n - 1) + [lst[-1] + lst[-2]]
