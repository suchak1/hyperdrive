import os
import pandas as pd
import yfinance as yf
from FileOps import FileReader, FileWriter

# MAKE market data class (broker=None):
# if broker, then use broker.get_hist else use default get_hist (tiingo?)


class MarketData:
    # all tiingo OR IEX CLOUD functions in here
    def __init__(self):
        self.writer = FileWriter()
        self.reader = FileReader()

    def get_symbols(self):
        return list(self.reader.load_csv('data/symbols.csv')['symbol'])

    def save_dividends(self, symbol):
        # given a symbol, save its dividend history
        df = self.get_dividends(symbol)
        self.writer.update_csv(f'data/dividends/{symbol.upper()}.csv', df)

    def save_splits(self, symbol):
        # given a symbol, save its stock split history
        df = self.get_splits(symbol)
        self.writer.update_csv(f'data/splits/{symbol.upper()}.csv', df)

# make tiingo OR IEX CLOUD!! version of get dividends which
# fetches existing dividend csv and adds a row if dividend
# today or fetches last 5 years, joins with existing and updates if new


class BrokerData(MarketData):
    def __init__(self, broker=None):
        super().__init__()
        self.broker = broker

    def get_dividends(self, symbol):
        # given a symbol, return the dividend history
        ticker = yf.Ticker(symbol.replace('.', '-'))
        new = ticker.actions.reset_index().drop(
            'Stock Splits',
            axis=1
        )

        filename = f'data/dividends/{symbol.upper()}.csv'
        if os.path.exists(filename):
            old = self.reader.load_csv(filename)
            old['Date'] = pd.to_datetime(old['Date'])
            old = old[~old['Date'].isin(new['Date'])]
            new = old.append(new, ignore_index=True)

        df = new[new['Dividends'] != 0].sort_values(by=['Date'])
        return df

    def get_splits(self, symbol):
        # given a symbol, return the stock splits
        ticker = yf.Ticker(symbol.replace('.', '-'))
        df = ticker.actions.reset_index().drop(
            'Dividends',
            axis=1
        )
        df = df[df['Stock Splits'] != 0]
        return df
