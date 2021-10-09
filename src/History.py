import numpy as np
import pandas as pd
import vectorbt as vbt
import Constants as C
from scipy.signal import argrelextrema
from DataSource import MarketData


class Historian:
    def buy_and_hold(self, symbol, timeframe, provider='polygon'):
        # returns a portfolio
        md = MarketData()
        md.provider = provider
        ohlc = md.get_ohlc(symbol, timeframe)
        close = ohlc[C.CLOSE]
        portfolio = vbt.Portfolio.from_holding(
            close, init_cash=1000, freq='D')
        return portfolio

    # function to create portfolio from signals & closes

    def fill(self, arr, method='ffill', type='bool'):
        # forward fills or nearest fills an array
        df = pd.DataFrame(arr)
        s = df.iloc[:, 0]
        if method == 'ffill':
            s = s.fillna(method='ffill')
        s = pd.to_numeric(s)
        s = s.interpolate(method='nearest').astype(type)
        out = s.to_numpy().flatten()
        return out

    def get_optimal_signals(self, close, n=10, method='ffill'):
        # finds the optimal signals for an array of prices
        close = np.array(close)
        mins = argrelextrema(close, np.less_equal,
                             order=n)[0]
        maxs = argrelextrema(close, np.greater_equal,
                             order=n)[0]

        signals = np.empty_like(close, dtype='object')
        signals[:] = np.nan
        signals[mins] = True
        signals[maxs] = False

        return self.fill(signals, method=method)
