import yfinance as yf

# MAKE market data class (broker=None):
# if broker, then use broker.get_hist else use default get_hist (tiingo?)


class MarketData:
    # all tiingo functions in here
    pass


class BrokerData(MarketData):
    def __init__(self, broker):
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
