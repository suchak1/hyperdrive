import pandas as pd
from datetime import datetime, timedelta
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
            except Exception as e:
                print(f'{symbol} recent split fetch failed')
                raise e
            if len(recent):
                splits[symbol] = recent
        return splits

    def find_split_row(self, df, ex, ratio):
        # finds the first post-split row in a df
        finalists = []
        ratios = df[C.OPEN] / df[C.CLOSE].shift()
        buffer = 0.1
        candidates = (ratios > ratio * (1 - buffer)
                      ) & (ratios < ratio * (1 + buffer))

        candidate_indices = [idx for idx, candidate in enumerate(
            list(candidates)) if candidate]

        times = list(df[C.TIME])
        for idx in candidate_indices:
            candidate_date = pd.to_datetime(times[idx]).date()
            ex_date = ex.date()
            if (
                    candidate_date <= ex_date and
                    candidate_date >= (ex_date - timedelta(days=C.FEW))
            ):
                finalists.append(times[idx])

        num_finalists = len(finalists)
        if num_finalists:
            if num_finalists == 1:
                return finalists[0]
            else:
                raise Exception('Too many candidates for split row selection.')

    def apply_split(self, df, ex, ratio):
        # first, separate based on split date
        pre = df[df[C.TIME] < ex].copy(deep=True)
        post = df[df[C.TIME] >= ex].copy(deep=True)
        # alternatively,
        # post = df[~df[C.TIME].isin(pre[C.TIME])].copy(deep=True)

        # next, apply split
        div_cols = {C.VOL, C.TRADES}
        mult_cols = {C.OPEN, C.CLOSE, C.LOW, C.HIGH, C.AVG, C.DIV}
        columns = mult_cols.union(div_cols)
        for col in columns:
            if col in df:
                multiplier = ratio if col in mult_cols else 1 / ratio
                pre[col] = round(pre[col] * multiplier, 2)

        # finally, join and sort
        df = pre.append(post, ignore_index=True).sort_values(C.TIME)
        return df

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
            # split row is the C.TIME in df for the first row that has post-split data
            split_row = self.find_split_row(ohlc[symbol], ex, ratio)
            # replace ex in following rows with split row date/time
            # note that find split row calc is only valid for one data type (ohlc vs intra) and one provider
            # ie a single symbol + provider + data type df

            # save df after applying split
            # once ohlc is finished, optimize/generalize for intra, and then dividends (including find split row fx)
            row_before_ex_date = ohlc[symbol][ohlc[symbol]
                                              [C.TIME] < split_row].tail(1)
            row_on_ex_date = ohlc[symbol][ohlc[symbol]
                                          [C.TIME] == split_row]
            if len(row_before_ex_date) and len(row_on_ex_date):
                diff = (row_on_ex_date.drop([C.TIME], axis=1).iloc[0] /
                        row_before_ex_date.drop([C.TIME], axis=1).iloc[0])
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
                                               [C.TIME] < split_row].tail(1)
            row_on_ex_date = intra[symbol][intra[symbol]
                                           [C.TIME] >= split_row].head(1)

            print(row_before_ex_date)
            print(row_on_ex_date)
            if len(row_before_ex_date) and len(row_on_ex_date):
                diff = (row_on_ex_date.drop([C.TIME], axis=1).iloc[0] /
                        row_before_ex_date.drop([C.TIME], axis=1).iloc[0])
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

        # account for multiple splits that need to be applied
        # implement dry run
        # use current broken price data for unit tests

        # update dividend, ohlc (prices, volume, num trades), and intraday (prices, volume, num trades)
        # prices * ratio and vol or trades / ratio?

                pass
