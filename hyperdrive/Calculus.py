
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter


class Calculator:
    def avg(self, xs):
        return sum(xs) / len(xs)

    def find_centroid(self, points, method='mean'):
        components = points.T
        if method != 'mean':
            components = [
                [
                    min(component),
                    max(component)
                ]
                for component in components
            ]
        return [self.avg(component) for component in components]

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

    def cv(self, x, ddof=0):
        if type(x) == pd.Series:
            axis = 0
        else:
            axis = 1
        return x.std(axis=axis, ddof=ddof) / x.mean(axis=axis)

    def fib(self, n):
        if n <= 1:
            return [0]
        elif n == 2:
            return [0, 1]
        else:
            lst = self.fib(n - 1)
            return self.fib(n - 1) + [lst[-1] + lst[-2]]

    def find_plane(self, pt1, pt2, pt3):
        x1, y1, z1 = pt1
        x2, y2, z2 = pt2
        x3, y3, z3 = pt3

        a1 = x2 - x1
        b1 = y2 - y1
        c1 = z2 - z1
        a2 = x3 - x1
        b2 = y3 - y1
        c2 = z3 - z1
        a = b1 * c2 - b2 * c1
        b = a2 * c1 - a1 * c2
        c = a1 * b2 - b1 * a2
        d = (- a * x1 - b * y1 - c * z1)

        return a, b, c, d

    def eval_plane(self, pt, coeffs):
        x, y, z = pt
        a, b, c, d = coeffs
        return a * x + b * y + c * z + d
