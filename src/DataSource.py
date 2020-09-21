import os
import requests
import pandas as pd
from operator import attrgetter
from datetime import datetime, timedelta
from polygon import RESTClient
from dotenv import load_dotenv
from FileOps import FileReader, FileWriter
from Constants import PathFinder
import Constants as C

# MAKE market data class (broker=None):
# if broker, then use broker.get_hist else use default get_hist (tiingo?)


class MarketData:
    def __init__(self, broker=None):
        self.writer = FileWriter()
        self.reader = FileReader()
        self.finder = PathFinder()
        self.provider = 'iexcloud'

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
        df = self.get_dividends(**kwargs)
        self.writer.update_csv(
            self.finder.get_dividends_path(symbol, self.provider), df)

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
        df = self.get_splits(**kwargs)
        self.writer.update_csv(
            self.finder.get_splits_path(symbol, self.provider), df)

    def standardize_ohlc(self, symbol, df):
        full_mapping = dict(
            zip(
                ['date', 'open', 'high', 'low', 'close', 'volume'],
                [C.TIME, C.OPEN, C.HIGH, C.LOW, C.CLOSE, C.VOL]
            )
        )
        return self.standardize(
            symbol,
            df,
            full_mapping,
            self.finder.get_ohlc_path,
            [C.TIME, C.OPEN, C.HIGH, C.LOW, C.CLOSE],
            0
        )

    def save_ohlc(self):
        # TODO
        # if 1d: get_prev_ohlc, else: get_ohlc
        # get rid off get_prev_ohlc?
        pass

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
        sen_df = self.get_social_sentiment(**kwargs)
        vol_df = self.get_social_volume(**kwargs)

        if sen_df.empty and not vol_df.empty:
            df = vol_df
        elif not sen_df.empty and vol_df.empty:
            df = sen_df
        elif not sen_df.empty and not vol_df.empty:
            df = sen_df.merge(vol_df, how="outer", on=C.TIME)
        else:
            return

        self.writer.update_csv(
            self.finder.get_sentiment_path(symbol), df)

    def standardize_sentiment(self, symbol, df):
        full_mapping = dict(
            zip(
                ['timestamp', 'bullish', 'bearish'],
                [C.TIME, C.POS, C.NEG]
            )
        )
        return self.standardize(
            symbol,
            df,
            full_mapping,
            self.finder.get_sentiment_path,
            [C.TIME, C.POS, C.NEG],
            0
        )

    def standardize_volume(self, symbol, df):
        full_mapping = dict(
            zip(
                ['timestamp', 'volume_score', 'volume_change'],
                [C.TIME, C.VOL, C.DELTA]
            )
        )
        return self.standardize(
            symbol,
            df,
            full_mapping,
            self.finder.get_sentiment_path,
            [C.TIME, C.VOL, C.DELTA],
            0
        )

    # def handle_request(self, url, err_msg):


class IEXCloud(MarketData):
    def __init__(self, broker=None):
        super().__init__(broker=broker)
        load_dotenv()
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

    def get_dividends(self, symbol, timeframe='3m'):
        # given a symbol, return the dividend history
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
            # self.writer.save_json(f'data/{symbol}.json', data)
        else:
            print(f'Invalid response from IEX for {symbol} dividends.')

        if not response.ok or data == []:
            return empty

        df = pd.DataFrame(data)

        return self.standardize_dividends(symbol, df)

    def get_splits(self, symbol, timeframe='3m'):
        # given a symbol, return the stock splits
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
            print(f'Invalid response from IEX for {symbol} splits.')

        if not response.ok or data == []:
            return empty

        df = pd.DataFrame(data)

        return self.standardize_splits(symbol, df)

    def get_prev_ohlc(self, symbol):
        # given a symbol, return the prev day's ohlc
        category = 'stock'
        dataset = 'previous'
        parts = [
            self.base,
            self.version,
            category,
            symbol,
            dataset
        ]
        endpoint = self.get_endpoint(parts)
        response = requests.get(endpoint)
        empty = pd.DataFrame()

        if response.ok:
            data = response.json()
        else:
            print(f'Invalid response from IEX for {symbol} splits.')

        if not response.ok or data == []:
            return empty

        df = pd.DataFrame([data])

        return self.standardize_ohlc(symbol, df)

    def get_ohlc(self, symbol, timeframe):
        pass

    def get_intraday(self):
        pass


class Polygon(MarketData):
    def __init__(self, broker=None):
        super().__init__(broker=broker)
        load_dotenv()
        self.client = RESTClient(os.environ['APCA_API_KEY_ID'])
        self.provider = 'polygon'

    def get_dividends(self, symbol, timeframe='max'):
        response = self.client.reference_stock_dividends(symbol)
        raw = pd.DataFrame(response.results)
        df = self.standardize_dividends(symbol, raw)
        return self.reader.data_in_timeframe(df, C.EX, timeframe)

    def get_splits(self, symbol, timeframe='max'):
        response = self.client.reference_stock_splits(symbol)
        raw = pd.DataFrame(response.results)
        df = self.standardize_splits(symbol, raw)
        return self.reader.data_in_timeframe(df, C.EX, timeframe)

    def get_prev_ohlc(self, symbol):
        today = datetime.today()
        one_day = timedelta(days=1)
        yesterday = today - one_day
        formatted_date = yesterday.strftime('%Y-%m-%d')
        response = self.client.stocks_equities_daily_open_close(
            symbol, formatted_date)
        raw = attrgetter('from_', 'open', 'high', 'low',
                         'close', 'volume')(response)
        labels = ['date', 'open', 'high', 'low', 'close', 'volume']
        data = dict(zip(labels, raw))
        df = pd.DataFrame([data])
        return self.standardize_ohlc(symbol, df)

    def get_ohlc(self, symbol, timeframe):
        pass

    def get_intraday(self):
        # all 1 min and 5 min ticks?
        pass
# newShares = oldShares / ratio


class StockTwits(MarketData):
    def __init__(self, broker=None):
        super().__init__(broker=broker)
        load_dotenv()
        self.provider = 'stocktwits'
        self.token = os.environ.get('STOCKTWITS')

    def get_social_volume(self, symbol, timeframe='max'):
        vol_res = requests.get(
            f"""
            https://api.stocktwits.com/api/2/symbols/{symbol}/volume.json?access_token={self.token}
            """)
        empty = pd.DataFrame()

        if vol_res.ok:
            vol_data = vol_res.json()['data']
        else:
            print(f'Invalid response from Stocktwits for {symbol}')

        if not vol_res.ok or vol_data == []:
            return empty

        # vol_data = json.load(open('../data/volume.json')
        #                      )['data']  # remove this
        vol_data.sort(key=lambda x: x['timestamp'])
        vol_data.pop()
        df = pd.DataFrame(vol_data)
        std = self.standardize_volume(symbol, df)
        filtered = self.reader.data_in_timeframe(std, C.TIME, timeframe)
        return filtered

    def get_social_sentiment(self, symbol, timeframe='max'):
        sen_res = requests.get(
            f'https://api.stocktwits.com/api/2/symbols/{symbol}/sentiment.json')

        empty = pd.DataFrame()

        if sen_res.ok:
            sen_data = sen_res.json()['data']
        else:
            print(f'Invalid response from Stocktwits for {symbol}.')

        if not sen_res.ok or sen_data == []:
            return empty

        # sen_data = json.load(open('../data/sentiment.json')
        #                      )['data']  # remove this
        sen_data.sort(key=lambda x: x['timestamp'])
        sen_data.pop()
        df = pd.DataFrame(sen_data)
        std = self.standardize_sentiment(symbol, df)
        filtered = self.reader.data_in_timeframe(std, C.TIME, timeframe)
        return filtered


# stocktwits
# import requests
# import json
# res = request.get('https://stocktwits.com/symbol/TSLA')
# start = res.text.find('sentimentChange')
# end = start + res.text[start:].find(',')
# sent = json.loads(f'{{"{res.text[start:end]}}}')
# also look into message volume and note initial sentiment and volume then record every day

# better way! https://api.stocktwits.com/api/2/symbols/TSLA/sentiment.json
# (but disregard / strip current date)
# https://api.stocktwits.com/api/2/symbols/TSLA/volume.json
# (but disregard / strip current date)
