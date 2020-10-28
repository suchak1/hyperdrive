import os
import requests
from time import sleep
import pandas as pd
from pytz import timezone
from operator import attrgetter
from datetime import datetime, timedelta
from polygon import RESTClient
from dotenv import load_dotenv
from FileOps import FileReader, FileWriter
from Constants import PathFinder
import Constants as C


class MarketData:
    def __init__(self):
        self.writer = FileWriter()
        self.reader = FileReader()
        self.finder = PathFinder()
        self.provider = 'iexcloud'

    def try_again(self, func, **kwargs):
        retries = (kwargs['retries']
                   if 'retries' in kwargs
                   else C.DEFAULT_RETRIES)
        delay = (kwargs['delay']
                 if 'delay' in kwargs
                 else C.DEFAULT_DELAY)
        func_args = {k: v for k, v in kwargs.items() if k not in {
            'retries', 'delay'}}
        for retry in range(retries):
            try:
                return func(**func_args)
            except Exception as e:
                if retry == retries - 1:
                    raise e
                else:
                    sleep(delay)

    def get_symbols(self):
        # get cached list of symbols
        symbols_path = self.finder.get_symbols_path()
        return list(self.reader.load_csv(symbols_path)[C.SYMBOL])

    def get_dividends(self, symbol, timeframe='max'):
        # given a symbol, return a cached dataframe
        df = self.reader.load_csv(
            self.finder.get_dividends_path(symbol, self.provider))
        filtered = self.reader.data_in_timeframe(df, C.EX, timeframe)
        return filtered

    def standardize(self, symbol, df, full_mapping, fx, columns, default):
        mapping = {k: v for k, v in full_mapping.items() if k in df}

        df = df[list(mapping)].rename(columns=mapping)
        filename = fx(symbol, self.provider)
        time_col, val_cols = columns[0], columns[1:]

        if time_col in df and set(val_cols).issubset(df.columns):
            df = self.reader.update_df(
                filename, df, time_col).sort_values(by=[time_col])
            # since time col is pd.datetime,
            # consider converting to YYYY-MM-DD str format
            for val_col in val_cols:
                df[val_col] = df[val_col].apply(
                    lambda val: float(val) if val else default)

        return df

    def standardize_dividends(self, symbol, df):
        full_mapping = dict(
            zip(
                ['exDate', 'paymentDate', 'declaredDate', 'amount'],
                [C.EX, C.PAY, C.DEC, C.DIV]
            )
        )
        return self.standardize(
            symbol,
            df,
            full_mapping,
            self.finder.get_dividends_path,
            [C.EX, C.DIV],
            0
        )

    def save_dividends(self, **kwargs):
        # given a symbol, save its dividend history
        symbol = kwargs['symbol']
        filename = self.finder.get_dividends_path(symbol, self.provider)
        df = self.reader.update_df(
            filename, self.get_dividends(**kwargs), C.EX)
        self.writer.update_csv(filename, df)

    def get_splits(self, symbol, timeframe='max'):
        # given a symbol, return a cached dataframe
        df = self.reader.load_csv(
            self.finder.get_splits_path(symbol, self.provider))
        filtered = self.reader.data_in_timeframe(df, C.EX, timeframe)
        return filtered

    def standardize_splits(self, symbol, df):
        full_mapping = dict(
            zip(
                ['exDate', 'paymentDate', 'declaredDate', 'ratio'],
                [C.EX, C.PAY, C.DEC, C.RATIO]
            )
        )
        return self.standardize(
            symbol,
            df,
            full_mapping,
            self.finder.get_splits_path,
            [C.EX, C.RATIO],
            1
        )

    def save_splits(self, **kwargs):
        # given a symbol, save its splits history
        symbol = kwargs['symbol']
        filename = self.finder.get_splits_path(symbol, self.provider)
        df = self.reader.update_df(filename, self.get_splits(**kwargs), C.EX)
        self.writer.update_csv(filename, df)

    def standardize_ohlc(self, symbol, df):
        full_mapping = dict(
            zip(
                ['date', 'open', 'high', 'low', 'close', 'volume'],
                [C.TIME, C.OPEN, C.HIGH, C.LOW, C.CLOSE, C.VOL]
            )
        )
        df = self.standardize(
            symbol,
            df,
            full_mapping,
            self.finder.get_ohlc_path,
            [C.TIME, C.OPEN, C.HIGH, C.LOW, C.CLOSE],
            0
        )

        if C.VOL in df:
            df[C.VOL] = df[C.VOL].apply(int)
        return df

    def get_ohlc(self, symbol, timeframe='max'):
        df = self.reader.load_csv(
            self.finder.get_ohlc_path(symbol, self.provider))
        filtered = self.reader.data_in_timeframe(df, C.TIME, timeframe)
        return filtered

    def save_ohlc(self, **kwargs):
        symbol = kwargs['symbol']
        filename = self.finder.get_ohlc_path(symbol, self.provider)
        df = self.reader.update_df(filename, self.get_ohlc(**kwargs), C.TIME)
        self.writer.update_csv(filename, df)

    def get_social_sentiment(self, symbol, timeframe='max'):
        # given a symbol, return a cached dataframe
        df = self.reader.load_csv(
            self.finder.get_sentiment_path(symbol))
        filtered = self.reader.data_in_timeframe(df, C.TIME, timeframe)[
            [C.TIME, C.POS, C.NEG]]
        return filtered

    def get_social_volume(self, symbol, timeframe='max'):
        # given a symbol, return a cached dataframe
        df = self.reader.load_csv(
            self.finder.get_sentiment_path(symbol))
        filtered = self.reader.data_in_timeframe(df, C.TIME, timeframe)[
            [C.TIME, C.VOL, C.DELTA]]
        return filtered

    def save_social_sentiment(self, **kwargs):
        # # given a symbol, save its sentiment data
        symbol = kwargs['symbol']
        filename = self.finder.get_sentiment_path(symbol)

        sen_df = self.reader.update_df(
            filename, self.get_social_sentiment(**kwargs), C.TIME)
        sen_df = sen_df[{C.TIME, C.POS, C.NEG}.intersection(sen_df.columns)]

        vol_df = self.reader.update_df(
            filename, self.get_social_volume(**kwargs), C.TIME)
        vol_df = vol_df[{C.TIME, C.VOL, C.DELTA}.intersection(vol_df.columns)]

        if sen_df.empty and not vol_df.empty:
            df = vol_df
        elif not sen_df.empty and vol_df.empty:
            df = sen_df
        elif not sen_df.empty and not vol_df.empty:
            df = sen_df.merge(vol_df, how="outer", on=C.TIME)
        else:
            return
        self.writer.update_csv(filename, df)

    def standardize_sentiment(self, symbol, df):
        full_mapping = dict(
            zip(
                ['timestamp', 'bullish', 'bearish'],
                [C.TIME, C.POS, C.NEG]
            )
        )
        df = self.standardize(
            symbol,
            df,
            full_mapping,
            self.finder.get_sentiment_path,
            [C.TIME, C.POS, C.NEG],
            0
        )
        return df[{C.TIME, C.POS, C.NEG}.intersection(df.columns)]

    def standardize_volume(self, symbol, df):
        full_mapping = dict(
            zip(
                ['timestamp', 'volume_score', 'volume_change'],
                [C.TIME, C.VOL, C.DELTA]
            )
        )
        df = self.standardize(
            symbol,
            df,
            full_mapping,
            self.finder.get_sentiment_path,
            [C.TIME, C.VOL, C.DELTA],
            0
        )
        return df[{C.TIME, C.VOL, C.DELTA}.intersection(df.columns)]

    def get_intraday(self, symbol, min=1, timeframe='max', extra_hrs=False):
        # implement way to transform 1 min dataset to 5 min data
        #  or 30 or 60 should be flexible soln
        # implement way to only get market hours
        pass

    def standardize_intraday(self):
        pass

    def save_intraday(self):
        pass
    # def handle_request(self, url, err_msg):


class IEXCloud(MarketData):
    def __init__(self):
        load_dotenv()
        super().__init__()
        self.base = 'https://cloud.iexapis.com'
        self.version = 'stable'
        self.token = os.environ['IEXCLOUD']
        self.provider = 'iexcloud'

    def get_endpoint(self, parts, raw_params=[]):
        # given a url
        # return an authenticated endpoint
        url = '/'.join(parts)
        auth_params = raw_params + [f'token={self.token}']
        params = '&'.join(auth_params)
        endpoint = f'{url}?{params}'
        return endpoint

    def get_dividends(self, **kwargs):
        # given a symbol, return the dividend history
        def _get_dividends(symbol, timeframe='3m'):
            category = 'stock'
            dataset = 'dividends'
            parts = [
                self.base,
                self.version,
                category,
                symbol.lower(),
                dataset,
                timeframe
            ]
            endpoint = self.get_endpoint(parts)
            response = requests.get(endpoint)
            empty = pd.DataFrame()

            if response.ok:
                data = [datum for datum in response.json() if datum['flag']
                        == 'Cash' and datum['currency'] == 'USD']
            else:
                raise Exception(
                    f'Invalid response from IEX for {symbol} dividends.')

            if data == []:
                return empty

            df = self.standardize_dividends(symbol, pd.DataFrame(data))
            return self.reader.data_in_timeframe(df, C.EX, timeframe)

        return self.try_again(func=_get_dividends, **kwargs)

    def get_splits(self, **kwargs):
        # given a symbol, return the stock splits
        def _get_splits(symbol, timeframe='3m'):
            category = 'stock'
            dataset = 'splits'
            parts = [
                self.base,
                self.version,
                category,
                symbol.lower(),
                dataset,
                timeframe
            ]
            endpoint = self.get_endpoint(parts)
            response = requests.get(endpoint)
            empty = pd.DataFrame()

            if response.ok:
                data = response.json()
            else:
                raise Exception(
                    f'Invalid response from IEX for {symbol} splits.')

            if data == []:
                return empty

            df = self.standardize_splits(symbol, pd.DataFrame(data))
            return self.reader.data_in_timeframe(df, C.EX, timeframe)

        return self.try_again(func=_get_splits, **kwargs)

    def get_ohlc(self, **kwargs):
        def _get_prev_ohlc(symbol):
            category = 'stock'
            dataset = 'previous'
            parts = [
                self.base,
                self.version,
                category,
                symbol.lower(),
                dataset
            ]
            endpoint = self.get_endpoint(parts)
            response = requests.get(endpoint)
            empty = pd.DataFrame()

            if response.ok:
                data = response.json()
            else:
                raise Exception(
                    f'Invalid response from IEX for {symbol} OHLC.')

            if data == []:
                return empty

            df = pd.DataFrame([data])
            return self.standardize_ohlc(symbol, df)

        def _get_ohlc(symbol, timeframe='1m'):
            if timeframe == '1d':
                return _get_prev_ohlc(symbol)

            category = 'stock'
            dataset = 'chart'
            parts = [
                self.base,
                self.version,
                category,
                symbol.lower(),
                dataset,
                timeframe
            ]
            endpoint = self.get_endpoint(parts)
            response = requests.get(endpoint)
            empty = pd.DataFrame()

            if response.ok:
                data = response.json()
            else:
                raise Exception(
                    f'Invalid response from IEX for {symbol} OHLC.')

            if data == []:
                return empty

            df = self.standardize_ohlc(symbol, pd.DataFrame(data))
            return self.reader.data_in_timeframe(df, C.TIME, timeframe)

        return self.try_again(func=_get_ohlc, **kwargs)

    # extra_hrs should be True if possible
    def get_intraday(self, symbol, min=1, timeframe='max', extra_hrs=True):
        # pass min directly into hist prices endpoint
        # to get 1, 5, 30, 60 min granularity if possible
        # and get extra hrs if possible
        pass
    # use historical prices endpoint


class Polygon(MarketData):
    def __init__(self, token=os.environ.get('APCA_API_KEY_ID')):
        load_dotenv()
        super().__init__()
        self.client = RESTClient(token)
        self.provider = 'polygon'

    def get_dividends(self, **kwargs):
        def _get_dividends(symbol, timeframe='max'):
            response = self.client.reference_stock_dividends(symbol)
            raw = pd.DataFrame(response.results)
            df = self.standardize_dividends(symbol, raw)
            return self.reader.data_in_timeframe(df, C.EX, timeframe)
        return self.try_again(func=_get_dividends, **kwargs)

    def get_splits(self, **kwargs):
        def _get_splits(symbol, timeframe='max'):
            response = self.client.reference_stock_splits(symbol)
            raw = pd.DataFrame(response.results)
            df = self.standardize_splits(symbol, raw)
            return self.reader.data_in_timeframe(df, C.EX, timeframe)
        return self.try_again(func=_get_splits, **kwargs)

    def get_ohlc(self, **kwargs):
        def _get_prev_ohlc(symbol):
            today = datetime.now(timezone('US/Eastern'))
            one_day = timedelta(days=1)
            yesterday = today - one_day
            formatted_date = yesterday.strftime('%Y-%m-%d')
            response = self.client.stocks_equities_daily_open_close(
                symbol, formatted_date, unadjusted=False)
            raw = attrgetter('from_', 'open', 'high', 'low',
                             'close', 'volume')(response)
            labels = ['date', 'open', 'high', 'low', 'close', 'volume']
            data = dict(zip(labels, raw))
            df = pd.DataFrame([data])
            return self.standardize_ohlc(symbol, df)

        def _get_ohlc(symbol, timeframe='max'):
            if timeframe == '1d':
                return _get_prev_ohlc(symbol)
            end = datetime.now(timezone('US/Eastern'))
            delta = self.reader.convert_delta(timeframe)
            start = end - delta
            formatted_start = start.strftime('%Y-%m-%d')
            formatted_end = end.strftime('%Y-%m-%d')
            response = self.client.stocks_equities_aggregates(
                symbol, 1, 'day',
                from_=formatted_start, to=formatted_end, unadjusted=False
            ).results
            columns = {'t': 'date', 'o': 'open', 'h': 'high',
                       'l': 'low', 'c': 'close', 'v': 'volume'}
            df = pd.DataFrame(response).rename(columns=columns)
            df['date'] = df['date'].apply(
                lambda x: datetime.fromtimestamp(int(x)/1000))
            df = self.standardize_ohlc(symbol, df)
            return self.reader.data_in_timeframe(df, C.TIME, timeframe)

        return self.try_again(func=_get_ohlc, **kwargs)

    def get_intraday(self, symbol, min=1, timeframe='max', extra_hrs=True):
        # pass min directly into stock_aggs function as multiplier
        pass
# newShares = oldShares / ratio


class StockTwits(MarketData):
    def __init__(self):
        load_dotenv()
        super().__init__()
        self.provider = 'stocktwits'
        self.token = os.environ.get('STOCKTWITS')

    def get_social_volume(self, **kwargs):
        def _get_social_volume(symbol, timeframe='max'):
            vol_res = requests.get((
                f'https://api.stocktwits.com/api/2/symbols/{symbol}'
                f'/volume.json?access_token={self.token}'
            ))
            empty = pd.DataFrame()

            if vol_res.ok:
                vol_data = vol_res.json()['data']
            else:
                raise Exception(
                    f'Invalid response from Stocktwits for {symbol}')

            if vol_data == []:
                return empty

            vol_data.sort(key=lambda x: x['timestamp'])
            vol_data.pop()
            df = pd.DataFrame(vol_data)
            std = self.standardize_volume(symbol, df)
            if timeframe == '1d':
                filtered = std.tail(1)
            else:
                filtered = self.reader.data_in_timeframe(
                    std, C.TIME, timeframe)
                [[C.TIME, C.VOL, C.DELTA]]
            return filtered

        return self.try_again(func=_get_social_volume, **kwargs)

    def get_social_sentiment(self, **kwargs):
        def _get_social_sentiment(symbol, timeframe='max'):
            sen_res = requests.get((
                f'https://api.stocktwits.com/api/2/symbols/{symbol}'
                f'/sentiment.json?access_token={self.token}'
            ))
            empty = pd.DataFrame()

            if sen_res.ok:
                sen_data = sen_res.json()['data']
            else:
                raise Exception(
                    f'Invalid response from Stocktwits for {symbol}.')

            if sen_data == []:
                return empty

            sen_data.sort(key=lambda x: x['timestamp'])
            sen_data.pop()
            df = pd.DataFrame(sen_data)
            std = self.standardize_sentiment(symbol, df)
            if timeframe == '1d':
                filtered = std.tail(1)
            else:
                filtered = self.reader.data_in_timeframe(
                    std, C.TIME, timeframe)
            return filtered
        return self.try_again(func=_get_social_sentiment, **kwargs)
