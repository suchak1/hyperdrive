import pandas as pd
from DataSource import MarketData  # noqa autopep8
import Constants as C  # noqa autopep8


def avg(xs):
    return sum(xs) / len(xs)


class SplitWorker:
    def __init__(self):
        self.md = MarketData()

    def get_recent_splits(self, symbols, timeframe):
        splits = {}
        for symbol in symbols:
            try:
                recent = self.md.get_splits(symbol, timeframe)
            except:
                print(f'{symbol} split fetch failed')
                # raise
            if len(recent):
                splits[symbol] = recent
        return splits

    def process(self, symbols=MarketData().get_symbols(),
                timeframe='3m', provider='iexcloud'):
        self.md.provider = provider

        ohlc = {}
        intra = {}
        div = {}
        splits = self.get_recent_splits(symbols, timeframe)
        pass
