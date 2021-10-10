import numpy as np
import pandas as pd
import vectorbt as vbt
import Constants as C
from scipy.signal import argrelextrema
from DataSource import MarketData
from sklearn.model_selection import train_test_split


class Historian:
    def buy_and_hold(self, symbol, timeframe, provider='polygon'):
        # returns a portfolio based on buy and hold strategy
        md = MarketData()
        md.provider = provider
        ohlc = md.get_ohlc(symbol, timeframe)
        close = ohlc[C.CLOSE]
        portfolio = vbt.Portfolio.from_holding(
            close, init_cash=1000, freq='D')
        return portfolio

    def create_portfolio(self, close, signals):
        # returns a portfolio based on signals
        portfolio = vbt.Portfolio.from_signals(
            close, signals, ~signals, init_cash=1000, freq='D'
        )
        return portfolio

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

    def generate_random(self, close, num=10**4):
        # generate random strategies
        good_signals = []
        portfolios = []
        sortinos = []
        calmars = []
        num_strats = num
        top_n = 25
        prob = self.get_optimal_signals(close).mean()

        for _ in range(num_strats):
            signals = pd.DataFrame.vbt.signals.generate_random(
                (len(close), 1), prob=prob)[0]
            portfolio = vbt.Portfolio.from_signals(
                close, signals, ~signals, init_cash=1000, freq='D')
            sortinos.append(portfolio.sortino_ratio())
            calmars.append(portfolio.calmar_ratio())
            good_signals.append(signals)
            portfolios.append(portfolio)

        top_s = set(np.argpartition(sortinos, -top_n)[-top_n:])
        top_c = set(np.argpartition(calmars, -top_n)[-top_n:])
        top_idxs = top_s.intersection(top_c)

        portfolios = [portfolio for idx, portfolio in enumerate(
            portfolios) if idx in top_idxs]
        good_signals = [signal for idx, signal in enumerate(
            good_signals) if idx in top_idxs]
        return good_signals

    def undersample(self, X, y, to_skip=13):
        # undersample and split train / test data
        df = pd.DataFrame(X)
        df['y'] =
        X = X.tail(len(X) - to_skip)
        y = pd.DataFrame(y)
        y = y.tail(len(y) - to_skip)
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=.2)
        train_true = 0
        train_false = 0
        X_train_new = []
        y_train_new = []
        train_num = len(y_train) - sum(y_train)
        for idx, y in enumerate(y_train):
            if y and train_true < train_num:
                X_train_new.append(X_train[idx])
                y_train_new.append(y_train[idx])
                train_true += 1
            elif not y and train_false < train_num:
                X_train_new.append(X_train[idx])
                y_train_new.append(y_train[idx])
                train_false += 1
        X_train = X_train_new
        y_train = y_train_new

        return X_train, X_test, y_train, y_test
    # def run classifiers

    # def plot_2d combos:

    # def plot 3d combos
