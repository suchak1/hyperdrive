
import yfinance as yf

# MAKE market data class (broker=None):
# if broker, then use broker.get_hist else use default get_hist (tiingo?)


class MarketData:
    def get_dividends(self, symbol):
        # given a symbol,
        # return the dividend history
        ticker = yf.Ticker(symbol)
        return ticker.actions


class BrokerData(MarketData):
    def __init__(self, broker):
        self.broker = broker
