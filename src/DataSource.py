import yfinance as yf
from FileOps import FileWriter

# MAKE market data class (broker=None):
# if broker, then use broker.get_hist else use default get_hist (tiingo?)


class MarketData:
    # all tiingo OR IEX CLOUD functions in here
    def __init__(self):
        self.writer = FileWriter()

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
    def __init__(self, broker):
        super().__init__()
        self.broker = broker

    def get_dividends(self, symbol):
        # given a symbol, return the dividend history
        ticker = yf.Ticker(symbol)
        df = ticker.actions.reset_index().drop(
            'Stock Splits',
            axis=1
        )
        return df

    def get_splits(self, symbol):
        # given a symbol, return the stock splits
        ticker = yf.Ticker(symbol)
        df = ticker.actions.reset_index().drop(
            'Dividends',
            axis=1
        )
        return df
