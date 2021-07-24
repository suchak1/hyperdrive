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

    def find_split_row(self, df, ex, ratio):
        new_df = df.drop([C.TIME], axis=1)
        # for compare all fields approach
        # ratio_df = new_df / new_df.shift()
        # for open/close ratio approach
        # (check 1.0 ratio for surrounding days as well)
        ratio_df = new_df[C.OPEN] / new_df[C.CLOSE].shift()
        # check if trades col, assign inverse
        # find split row (majority columns fit in ratio threshold)
        # see if row is within few days of ex-date
        # return row or None
        pass

    def process(self, symbols=MarketData().get_symbols(),
                timeframe='3m', provider='iexcloud'):
        self.md.provider = provider

        ohlc = {}
        intra = {}
        div = {}
        splits = self.get_recent_splits(symbols, timeframe)
        liberal_timeframe = C.FEW_DAYS
        for symbol in splits:
            print(symbol)
            # print(splits[symbol])
            liberal_timeframe = self.md.traveller.add_timeframes(
                [timeframe, C.FEW_DAYS, '1d'])
            ohlc[symbol] = self.md.get_ohlc(symbol, liberal_timeframe)
            intra[symbol] = pd.concat(
                self.md.get_intraday(symbol, timeframe=liberal_timeframe))
            div[symbol] = self.md.get_dividends(symbol, liberal_timeframe)

            last_split = splits[symbol].tail(1)
            ex = last_split[C.EX].iloc[0]
            ratio = last_split[C.RATIO].iloc[0]

            # OHLC
            split_row = self.find_split_row(ohlc[symbol], ex, ratio)

            row_before_ex_date = ohlc[symbol][ohlc[symbol]
                                              [C.TIME] < ex].tail(1)
            row_on_ex_date = ohlc[symbol][ohlc[symbol]
                                          [C.TIME] == ex]
            if len(row_before_ex_date) and len(row_on_ex_date):
                diff = row_on_ex_date.drop(
                    [C.TIME], axis=1).iloc[0] / row_before_ex_date.drop([C.TIME], axis=1).iloc[0]
                diff[C.VOL] = 1 / diff[C.VOL]
                if C.TRADES in diff:
                    diff[C.TRADES] = 1 / diff[C.TRADES]
                certainty = avg(abs(diff - ratio) < (ratio*0.1)) > 0.5

                if certainty:
                    # update ohlc
                    print(f'{symbol} needs to have OHLC adjusted for splits')

            # Intraday
            # need check to see if ex date is even in df - otherwise error single positional indexer is out-of-bounds
            row_before_ex_date = intra[symbol][intra[symbol]
                                               [C.TIME] < ex].tail(1)
            row_on_ex_date = intra[symbol][intra[symbol]
                                           [C.TIME] >= ex].head(1)

            print(row_before_ex_date)
            print(row_on_ex_date)
            if len(row_before_ex_date) and len(row_on_ex_date):
                diff = row_on_ex_date.drop(
                    [C.TIME], axis=1).iloc[0] / row_before_ex_date.drop([C.TIME], axis=1).iloc[0]
                diff[C.VOL] = 1 / diff[C.VOL]
                if C.TRADES in diff:
                    diff[C.TRADES] = 1 / diff[C.TRADES]
                # certainty = avg(abs(diff - ratio) < 0.02) > 0.5
                certainty = avg(abs(diff - ratio) < (ratio*0.1)) > 0.5

                if certainty:
                    # update intraday
                    print(f'{symbol} needs to have Intraday adjusted for splits')

            # Dividends
            # dividend logic here
            # this is a hard problem?
            # fetch dividends for last 5 years and check ratio
            # use dividends fetched from data broker as truth
            # if we have any dividends older than that,
            # check ratio between what we have and broker data
            # and then apply ratio to older data that broker won't give

        # implement few days smart check
        # implement split update
        # test w expected iexcloud and polygon updates => (
        #   AAPL div for poly and iex,
        #   NEE ohlc, intra, div for poly and iex
        #   CP ohlc, intra, div for poly and iex,
        #   NVDA ohlc, intra, div for both poly and iex)
        # write tests
        # make sure trades number is as expected for iexcloud and polygon (verify ratio)
        # use intraday specific logic
        # create scheduled workflow and have try catches

        # update dividend, ohlc (prices, volume, num trades), and intraday (prices, volume, num trades)
        # prices * ratio and vol or trades / ratio?

                pass
