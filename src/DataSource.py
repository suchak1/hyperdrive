import os
import requests
from time import sleep, time
import pandas as pd
from polygon import RESTClient
from dotenv import load_dotenv, find_dotenv
from FileOps import FileReader, FileWriter
from TimeMachine import TimeTraveller
from Constants import PathFinder
import Constants as C


class MarketData:
    def __init__(self):
        load_dotenv(find_dotenv('config.env'))
        self.writer = FileWriter()
        self.reader = FileReader()
        self.finder = PathFinder()
        self.traveller = TimeTraveller()
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

    def standardize(self, df, full_mapping,
                    filename, columns, default):
        mapping = {k: v for k, v in full_mapping.items() if k in df}

        df = df[list(mapping)].rename(columns=mapping)
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
        filename = self.finder.get_dividends_path(symbol, self.provider)
        return self.standardize(
            df,
            full_mapping,
            filename,
            [C.EX, C.DIV],
            0
        )

    def save_dividends(self, **kwargs):
        # given a symbol, save its dividend history
        symbol = kwargs['symbol']
        filename = self.finder.get_dividends_path(symbol, self.provider)
        if os.path.exists(filename):
            os.remove(filename)
        df = self.reader.update_df(
            filename, self.get_dividends(**kwargs), C.EX, C.DATE_FMT)
        self.writer.update_csv(filename, df)
        if os.path.exists(filename):
            return filename

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
        filename = self.finder.get_splits_path(symbol, self.provider)
        return self.standardize(
            df,
            full_mapping,
            filename,
            [C.EX, C.RATIO],
            1
        )

    def save_splits(self, **kwargs):
        # given a symbol, save its splits history
        symbol = kwargs['symbol']
        filename = self.finder.get_splits_path(symbol, self.provider)
        if os.path.exists(filename):
            os.remove(filename)
        df = self.reader.update_df(
            filename, self.get_splits(**kwargs), C.EX, C.DATE_FMT)
        self.writer.update_csv(filename, df)
        if os.path.exists(filename):
            return filename

    def standardize_ohlc(self, symbol, df, filename=None):
        full_mapping = dict(
            zip(
                ['date', 'open', 'high', 'low', 'close',
                 'volume', 'average', 'trades'],
                [C.TIME, C.OPEN, C.HIGH, C.LOW, C.CLOSE,
                 C.VOL, C.AVG, C.TRADES]
            )
        )

        filename = filename or self.finder.get_ohlc_path(symbol, self.provider)

        df = self.standardize(
            df,
            full_mapping,
            filename,
            [C.TIME, C.OPEN, C.HIGH, C.LOW, C.CLOSE],
            0
        )

        for col in [C.VOL, C.TRADES]:
            if col in df:
                df[col] = df[col].apply(
                    lambda val: 0 if pd.isnull(val) else int(val))

        return df

    def get_ohlc(self, symbol, timeframe='max'):
        df = self.reader.load_csv(
            self.finder.get_ohlc_path(symbol, self.provider))
        filtered = self.reader.data_in_timeframe(df, C.TIME, timeframe)
        return filtered

    def save_ohlc(self, **kwargs):
        symbol = kwargs['symbol']
        filename = self.finder.get_ohlc_path(symbol, self.provider)
        if os.path.exists(filename):
            os.remove(filename)
        df = self.reader.update_df(
            filename, self.get_ohlc(**kwargs), C.TIME, C.DATE_FMT)
        self.writer.update_csv(filename, df)
        if os.path.exists(filename):
            return filename

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

        if os.path.exists(filename):
            os.remove(filename)

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
        if os.path.exists(filename):
            return filename

    def standardize_sentiment(self, symbol, df):
        full_mapping = dict(
            zip(
                ['timestamp', 'bullish', 'bearish'],
                [C.TIME, C.POS, C.NEG]
            )
        )
        filename = self.finder.get_sentiment_path(symbol, self.provider)
        df = self.standardize(
            df,
            full_mapping,
            filename,
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
        filename = self.finder.get_sentiment_path(symbol, self.provider)
        df = self.standardize(
            df,
            full_mapping,
            filename,
            [C.TIME, C.VOL, C.DELTA],
            0
        )
        return df[{C.TIME, C.VOL, C.DELTA}.intersection(df.columns)]

    def get_intraday(self, symbol, min=1, timeframe='max', extra_hrs=False):
        # implement way to transform 1 min dataset to 5 min data
        #  or 30 or 60 should be flexible soln
        # implement way to only get market hours
        # given a symbol, return a cached dataframe
        dates = self.traveller.dates_in_range(timeframe)
        for date in dates:
            df = self.reader.load_csv(
                self.finder.get_intraday_path(symbol, date, self.provider))
            yield self.reader.data_in_timeframe(df, C.TIME, timeframe)

    def save_intraday(self, **kwargs):
        symbol = kwargs['symbol']
        dfs = self.get_intraday(**kwargs)
        filenames = []

        for df in dfs:
            date = df[C.TIME].iloc[0].strftime(C.DATE_FMT)
            filename = self.finder.get_intraday_path(
                symbol, date, self.provider)
            if os.path.exists(filename):
                os.remove(filename)
            save_fmt = f'{C.DATE_FMT} {C.TIME_FMT}'
            df = self.reader.update_df(
                filename, df, C.TIME, save_fmt)
            self.writer.update_csv(filename, df)
            if os.path.exists(filename):
                filenames.append(filename)
        return filenames

    def get_unemployment_rate(self, timeframe='max'):
        # given a timeframe, return a cached dataframe
        df = self.reader.load_csv(
            self.finder.get_unemployment_path())
        filtered = self.reader.data_in_timeframe(df, C.TIME, timeframe)
        return filtered

    def standardize_unemployment(self,  df):
        full_mapping = dict(
            zip(
                ['time', 'value'],
                [C.TIME, C.UN_RATE]
            )
        )
        filename = self.finder.get_unemployment_path()
        return self.standardize(
            df,
            full_mapping,
            filename,
            [C.TIME, C.UN_RATE],
            0
        )

    def save_unemployment_rate(self, **kwargs):
        # given a symbol, save its dividend history
        filename = self.finder.get_unemployment_path()
        if os.path.exists(filename):
            os.remove(filename)
        df = self.reader.update_df(
            filename, self.get_unemployment_rate(**kwargs), C.TIME, '%Y-%m')
        self.writer.update_csv(filename, df)
        if os.path.exists(filename):
            return filename

    def standardize_s2f_ratio(self, df):
        full_mapping = dict(
            zip(
                ['t', 'o.daysTillHalving', 'o.ratio'],
                [C.TIME, C.HALVING, C.RATIO]
            )
        )
        filename = self.finder.get_s2f_path()
        df = self.standardize(
            df,
            full_mapping,
            filename,
            [C.TIME, C.HALVING, C.RATIO],
            0
        )
        return df[{C.TIME, C.HALVING, C.RATIO}.intersection(df.columns)]

    def get_s2f_ratio(self, timeframe='max'):
        # given a symbol, return a cached dataframe
        df = self.reader.load_csv(
            self.finder.get_s2f_path())
        filtered = self.reader.data_in_timeframe(df, C.TIME, timeframe)[
            [C.TIME, C.HALVING, C.RATIO]]
        return filtered

    def save_s2f_ratio(self, **kwargs):
        # # given a symbol, save its s2f data
        filename = self.finder.get_s2f_path()

        if os.path.exists(filename):
            os.remove(filename)

        df = self.reader.update_df(
            filename, self.get_s2f_ratio(**kwargs), C.TIME, C.DATE_FMT)

        self.writer.update_csv(filename, df)
        if os.path.exists(filename):
            return filename

    def standardize_diff_ribbon(self, df):
        full_mapping = dict(
            zip(
                ['t', 'o.ma9', 'o.ma14', 'o.ma25', 'o.ma40',
                    'o.ma60', 'o.ma90', 'o.ma128', 'o.ma200'],
                [C.TIME, C.MA9, C.MA14, C.MA25, C.MA40,
                    C.MA60, C.MA90, C.MA128, C.MA200]
            )
        )
        filename = self.finder.get_diff_ribbon_path()
        df = self.standardize(
            df,
            full_mapping,
            filename,
            [C.TIME, C.MA9, C.MA14, C.MA25, C.MA40,
             C.MA60, C.MA90, C.MA128, C.MA200],
            0
        )
        return df[{C.TIME, C.MA9, C.MA14, C.MA25, C.MA40,
                   C.MA60, C.MA90, C.MA128, C.MA200}.intersection(df.columns)]

    def get_diff_ribbon(self, timeframe='max'):
        # given a symbol, return a cached dataframe
        df = self.reader.load_csv(
            self.finder.get_diff_ribbon_path())
        filtered = self.reader.data_in_timeframe(df, C.TIME, timeframe)[
            [C.TIME, C.MA9, C.MA14, C.MA25, C.MA40,
             C.MA60, C.MA90, C.MA128, C.MA200]]
        return filtered

    def save_diff_ribbon(self, **kwargs):
        # # given a symbol, save its s2f data
        filename = self.finder.get_diff_ribbon_path()

        if os.path.exists(filename):
            os.remove(filename)

        df = self.reader.update_df(
            filename, self.get_diff_ribbon(**kwargs), C.TIME, C.DATE_FMT)

        self.writer.update_csv(filename, df)
        if os.path.exists(filename):
            return filename

    def standardize_sopr(self, df):
        full_mapping = dict(
            zip(
                ['t', 'v'],
                [C.TIME, C.SOPR]
            )
        )
        filename = self.finder.get_diff_ribbon_path()
        df = self.standardize(
            df,
            full_mapping,
            filename,
            [C.TIME, C.SOPR],
            1
        )
        return df[{C.TIME, C.SOPR}.intersection(df.columns)]

    def get_sopr(self, timeframe='max'):
        # given a symbol, return a cached dataframe
        df = self.reader.load_csv(
            self.finder.get_sopr_path())
        filtered = self.reader.data_in_timeframe(df, C.TIME, timeframe)[
            [C.TIME, C.SOPR]]
        return filtered

    def save_sopr(self, **kwargs):
        # # given a symbol, save its s2f data
        filename = self.finder.get_sopr_path()

        if os.path.exists(filename):
            os.remove(filename)

        df = self.reader.update_df(
            filename, self.get_sopr(**kwargs), C.TIME, C.DATE_FMT)

        self.writer.update_csv(filename, df)
        if os.path.exists(filename):
            return filename
    # def handle_request(self, url, err_msg):


class IEXCloud(MarketData):
    def __init__(self):
        super().__init__()
        self.base = 'https://cloud.iexapis.com'
        self.version = 'v1'
        self.token = os.environ['IEXCLOUD']
        self.provider = 'iexcloud'

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
            url = '/'.join(parts)
            params = {'token': self.token}
            response = requests.get(url, params=params)
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
            url = '/'.join(parts)
            params = {'token': self.token}
            response = requests.get(url, params=params)
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
            url = '/'.join(parts)
            params = {'token': self.token}
            response = requests.get(url, params=params)
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
            url = '/'.join(parts)
            params = {'token': self.token}
            response = requests.get(url, params=params)
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
    def get_intraday(self, **kwargs):
        def _get_intraday(symbol, min=1, timeframe='max', extra_hrs=True):
            # pass min directly into hist prices endpoint
            # to get 1, 5, 30, 60 min granularity if possible
            # and get extra hrs if possible
            category = 'stock'
            dataset = 'chart'

            dates = self.traveller.dates_in_range(timeframe)
            if dates == []:
                raise Exception(f'No dates in timeframe: {timeframe}.')

            for date in dates:
                parts = [
                    self.base,
                    self.version,
                    category,
                    symbol.lower(),
                    dataset,
                    'date',
                    date.replace('-', '')
                ]

                url = '/'.join(parts)
                params = {'token': self.token}
                response = requests.get(url, params=params)

                if response.ok:
                    data = response.json()
                else:
                    raise Exception(
                        f'Invalid response from IEX for {symbol} intraday.')

                if data == []:
                    continue

                res_cols = ['date', 'minute', 'marketOpen', 'marketHigh',
                            'marketLow', 'marketClose', 'marketVolume',
                            'marketAverage', 'marketNumberOfTrades']
                std_cols = ['date', 'minute', 'open', 'high', 'low',
                            'close', 'volume', 'average', 'trades']

                columns = dict(zip(res_cols, std_cols))
                df = pd.DataFrame(data)[res_cols].rename(columns=columns)
                df['date'] = pd.to_datetime(df['date'] + ' ' + df['minute'])
                df.drop(columns='minute', inplace=True)
                filename = self.finder.get_intraday_path(
                    symbol, date, self.provider)
                df = self.standardize_ohlc(symbol, df, filename)
                yield df

        return self.try_again(func=_get_intraday, **kwargs)


class Polygon(MarketData):
    def __init__(self, token=os.environ.get('POLYGON'), free=True):
        super().__init__()
        self.client = RESTClient(token)
        self.provider = 'polygon'
        self.free = free

    def obey_free_limit(self):
        if self.free and hasattr(self, 'last_api_call_time'):
            time_since_last_call = time() - self.last_api_call_time
            delay = C.POLY_FREE_DELAY - time_since_last_call
            if delay > 0:
                sleep(delay)

    def log_api_call_time(self):
        self.last_api_call_time = time()

    def get_dividends(self, **kwargs):
        def _get_dividends(symbol, timeframe='max'):
            self.obey_free_limit()
            try:
                response = self.client.reference_stock_dividends(symbol)
            except Exception as e:
                raise e
            finally:
                self.log_api_call_time()
            raw = pd.DataFrame(response.results)
            df = self.standardize_dividends(symbol, raw)
            return self.reader.data_in_timeframe(df, C.EX, timeframe)
        return self.try_again(func=_get_dividends, **kwargs)

    def get_splits(self, **kwargs):
        def _get_splits(symbol, timeframe='max'):
            self.obey_free_limit()
            try:
                response = self.client.reference_stock_splits(symbol)
            except Exception as e:
                raise e
            finally:
                self.log_api_call_time()
            raw = pd.DataFrame(response.results)
            df = self.standardize_splits(symbol, raw)
            return self.reader.data_in_timeframe(df, C.EX, timeframe)
        return self.try_again(func=_get_splits, **kwargs)

    def get_ohlc(self, **kwargs):
        def _get_ohlc(symbol, timeframe='max'):
            is_crypto = symbol.find('X%3A') == 0
            formatted_start, formatted_end = self.traveller.convert_dates(
                timeframe)
            self.obey_free_limit()
            try:
                response = self.client.stocks_equities_aggregates(
                    symbol, 1, 'day',
                    from_=formatted_start, to=formatted_end, unadjusted=False
                )
            except Exception as e:
                raise e
            finally:
                self.log_api_call_time()
            raw = response.results
            columns = {'t': 'date', 'o': 'open', 'h': 'high',
                       'l': 'low', 'c': 'close', 'v': 'volume',
                       'vw': 'average', 'n': 'trades'}

            df = pd.DataFrame(raw).rename(columns=columns)
            if is_crypto:
                df['date'] = pd.to_datetime(
                    df['date'], unit='ms')
            else:
                df['date'] = pd.to_datetime(
                    df['date'], unit='ms').dt.tz_localize(
                    'UTC').dt.tz_convert(
                    C.TZ).dt.tz_localize(None)
            df = self.standardize_ohlc(symbol, df)
            return self.reader.data_in_timeframe(df, C.TIME, timeframe)

        return self.try_again(func=_get_ohlc, **kwargs)

    def get_intraday(self, **kwargs):
        def _get_intraday(symbol, min=1, timeframe='max', extra_hrs=True):
            # pass min directly into stock_aggs function as multiplier
            is_crypto = symbol.find('X%3A') == 0
            dates = self.traveller.dates_in_range(timeframe)
            if dates == []:
                raise Exception(f'No dates in timeframe: {timeframe}.')

            for idx, date in enumerate(dates):
                self.obey_free_limit()
                try:
                    response = self.client.stocks_equities_aggregates(
                        symbol, min, 'minute', from_=date, to=date,
                        unadjusted=False
                    )
                except Exception as e:
                    raise e
                finally:
                    self.log_api_call_time()

                if hasattr(response, 'results'):
                    response = response.results
                else:
                    continue

                columns = {'t': 'date', 'o': 'open', 'h': 'high',
                           'l': 'low', 'c': 'close', 'v': 'volume',
                           'vw': 'average', 'n': 'trades'}
                df = pd.DataFrame(response).rename(columns=columns)
                if is_crypto:
                    df['date'] = pd.to_datetime(
                        df['date'], unit='ms')
                else:
                    df['date'] = pd.to_datetime(
                        df['date'], unit='ms').dt.tz_localize(
                        'UTC').dt.tz_convert(
                        C.TZ).dt.tz_localize(None)
                filename = self.finder.get_intraday_path(
                    symbol, date, self.provider)
                df = self.standardize_ohlc(symbol, df, filename)
                df = df[df[C.TIME].dt.strftime(C.DATE_FMT) == date]
                yield df

        return self.try_again(func=_get_intraday, **kwargs)


# newShares = oldShares / ratio


class StockTwits(MarketData):
    def __init__(self):
        super().__init__()
        self.base = 'https://api.stocktwits.com'
        self.version = '2'
        self.token = os.environ.get('STOCKTWITS')
        self.provider = 'stocktwits'

    def get_social_volume(self, **kwargs):
        def _get_social_volume(symbol, timeframe='max'):
            parts = [
                self.base,
                'api',
                self.version,
                'symbols',
                symbol,
                'volume.json'
            ]
            url = '/'.join(parts)
            params = {'access_token': self.token}
            vol_res = requests.get(url, params=params)
            json_res = vol_res.json()
            empty = pd.DataFrame()

            if vol_res.ok:
                vol_data = json_res['data']
            else:
                if 'errors' in json_res:
                    errors = '\n'.join([error['message']
                                        for error in json_res['errors']])
                raise Exception(
                    f'Invalid response from Stocktwits for {symbol}\n{errors}')

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
            parts = [
                self.base,
                'api',
                self.version,
                'symbols',
                symbol,
                'sentiment.json'
            ]
            url = '/'.join(parts)
            params = {'access_token': self.token}
            sen_res = requests.get(url, params=params)
            json_res = sen_res.json()
            empty = pd.DataFrame()

            if sen_res.ok:
                sen_data = json_res['data']
            else:
                if 'errors' in json_res:
                    errors = '\n'.join([error['message']
                                        for error in json_res['errors']])
                raise Exception(
                    f'Invalid response from Stocktwits for {symbol}\n{errors}')

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


class LaborStats(MarketData):
    def __init__(self):
        super().__init__()
        self.base = 'https://api.bls.gov'
        self.version = 'v2'
        self.token = os.environ.get('BLS')
        self.provider = 'bls'

    def get_unemployment_rate(self, **kwargs):
        def _get_unemployment_rate(timeframe):
            start, end = self.traveller.convert_dates(timeframe, '%Y')

            parts = [
                self.base,
                'publicAPI',
                self.version,
                'timeseries',
                'data'
            ]
            url = '/'.join(parts)
            params = {'registrationkey': self.token,
                      'startyear': start, 'endyear': end,
                      'seriesid': 'LNS14000000'}

            response = requests.post(url, data=params)

            if (
                    response.ok and
                    response.json()['status'] == 'REQUEST_SUCCEEDED'
            ):

                payload = response.json()
                if payload['status'] == 'REQUEST_SUCCEEDED':
                    data = payload['Results']['series'][0]['data']
                else:
                    raise Exception(
                        f'''
                        Invalid response from BLS because {data["message"][0]}
                        '''
                    )
            else:
                raise Exception(
                    'Invalid response from BLS for unemployment rate')

            df = pd.DataFrame(data)
            df['time'] = df['year'] + '-' + \
                df['period'].str.slice(start=1)

            df = self.standardize_unemployment(df)
            return self.reader.data_in_timeframe(df, C.TIME, timeframe)

        return self.try_again(func=_get_unemployment_rate, **kwargs)


class Glassnode(MarketData):
    def __init__(self):
        super().__init__()
        self.base = 'https://api.glassnode.com'
        self.version = 'v1'
        self.token = os.environ.get('GLASSNODE')
        self.provider = 'glassnode'

    def get_s2f_ratio(self, **kwargs):
        def _get_s2f_ratio(timeframe):
            parts = [
                self.base,
                self.version,
                'metrics',
                'indicators',
                'stock_to_flow_ratio'
            ]
            url = '/'.join(parts)
            empty = pd.DataFrame()
            response = requests.get(
                url, params={'a': 'BTC', 'api_key': self.token})

            if response.ok:
                data = response.json()
            else:
                raise Exception(
                    'Invalid response from Glassnode for S2F Ratio')

            if data == []:
                return empty

            df = pd.json_normalize(data)
            df['t'] = pd.to_datetime(df['t'], unit='s')
            df = self.standardize_s2f_ratio(df)
            return self.reader.data_in_timeframe(df, C.TIME, timeframe)

        return self.try_again(func=_get_s2f_ratio, **kwargs)

    def get_diff_ribbon(self, **kwargs):
        def _get_diff_ribbon(timeframe):
            parts = [
                self.base,
                self.version,
                'metrics',
                'indicators',
                'difficulty_ribbon'
            ]
            url = '/'.join(parts)
            empty = pd.DataFrame()
            response = requests.get(
                url, params={'a': 'BTC', 'api_key': self.token})

            if response.ok:
                data = response.json()
            else:
                raise Exception(
                    'Invalid response from Glassnode for Difficulty Ribbon')

            if data == []:
                return empty

            df = pd.json_normalize(data)
            df['t'] = pd.to_datetime(df['t'], unit='s')
            df = self.standardize_diff_ribbon(df)
            return self.reader.data_in_timeframe(df, C.TIME, timeframe)

        return self.try_again(func=_get_diff_ribbon, **kwargs)

    def get_sopr(self, **kwargs):
        def _get_sopr(timeframe):
            parts = [
                self.base,
                self.version,
                'metrics',
                'indicators',
                'sopr'
            ]
            url = '/'.join(parts)
            empty = pd.DataFrame()
            response = requests.get(
                url, params={'a': 'BTC', 'api_key': self.token})

            if response.ok:
                data = response.json()
            else:
                raise Exception(
                    'Invalid response from Glassnode for SOPR')

            if data == []:
                return empty

            df = pd.json_normalize(data)
            df['t'] = pd.to_datetime(df['t'], unit='s')
            df = self.standardize_sopr(df)
            return self.reader.data_in_timeframe(df, C.TIME, timeframe)

        return self.try_again(func=_get_sopr, **kwargs)
