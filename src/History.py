import vectorbt as vbt
import Constants as C
from DataSource import MarketData


class Historian:
    def buy_and_hold(self, symbol, timeframe, provider='polygon'):
        md = MarketData()
        md.provider = provider
        ohlc = md.get_ohlc(symbol, timeframe)
        closes = ohlc[C.CLOSE]
        portfolio = vbt.Portfolio.from_holding(
            closes, init_cash=1000, freq='D')
        return portfolio.stats()
