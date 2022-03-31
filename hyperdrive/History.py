import numpy as np
import pandas as pd
import vectorbt as vbt
from scipy.signal import argrelextrema
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from Calculus import Calculator


class Historian:
    def __init__(self):
        self.calc = Calculator()

    # add fx to perform calculations on columns
    # takes calc.fx, df, and column names as args, fx args

    def buy_and_hold(self, close, init_cash=1000):
        # returns a portfolio based on buy and hold strategy
        portfolio = vbt.Portfolio.from_holding(
            close, init_cash=init_cash, freq='D')
        return portfolio

    def create_portfolio(self, close, signals, init_cash=1000, fee=0):
        # returns a portfolio based on signals
        portfolio = vbt.Portfolio.from_signals(
            close, signals, ~signals, init_cash=init_cash, freq='D', fees=fee
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

    def unfill(self, xs):
        if not len(xs):
            return xs
        curr = xs[0]
        new = [curr]
        for x in xs[1:]:
            if curr != x:
                new.append(x)
                curr = x
            else:
                new.append(None)
        return new

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

    def split(self, X, y):
        df = pd.DataFrame(X)
        df['y'] = y
        df = df.dropna()
        y = df['y'].to_numpy()
        X = df.drop('y', axis=1).to_numpy()
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=.2)
        return X_train, X_test, y_train, y_test

    def oversample(self, X_train, y_train):
        sm = SMOTE()
        X_res, y_res = sm.fit_resample(X_train, y_train)
        return X_res, y_res

    def preprocess(self, X, y, num_pca=2):
        X_train, X_test, y_train, y_test = self.split(X, y)
        X_train, y_train = self.oversample(X_train, y_train)
        X_train, X_test, scaler = self.standardize(X_train, X_test)
        if num_pca:
            X_train, X_test, pca = self.pca(X_train, num_pca, X_test)
        else:
            pca = None
        X, full_scaler = self.standardize(X)
        if num_pca:
            X, full_pca = self.pca(X, num_pca)
        else:
            full_pca = None

        return (
            X_train, X_test, y_train, y_test,
            X, y, scaler, pca, full_scaler, full_pca
        )

    def standardize(self, X_train, X_test=None):
        scaler = StandardScaler().fit(X_train)
        X_train = scaler.transform(X_train)
        if type(X_test) == np.ndarray:
            X_test = scaler.transform(X_test)
            return X_train, X_test, scaler
        return X_train, scaler

    def pca(self, X_train, n, X_test=None):
        num_features = X_train.shape[1]
        n = n if n <= num_features else num_features
        pca = PCA(n_components=n).fit(X_train)
        X_train = pca.transform(X_train)
        if type(X_test) == np.ndarray:
            X_test = pca.transform(X_test)
            var = pca.explained_variance_ratio_.sum() * 100
            print(f'Explained variance (X_train): {round(var, 2)}%')
            return X_train, X_test, pca
        var = pca.explained_variance_ratio_.sum() * 100
        print(f'Explained variance (X): {round(var, 2)}%')
        return X_train, pca
