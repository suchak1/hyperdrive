import os
import requests
import pandas as pd
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

    def standardize_dividends(self, symbol, df):
        full_mapping = dict(
            zip(
                ['exDate', 'paymentDate', 'declaredDate', 'amount'],
                [C.EX, C.PAY, C.DEC, C.DIV]
            )
        )
        mapping = {k: v for k, v in full_mapping.items() if k in df}
        columns = list(mapping)

        df = df[columns].rename(columns=mapping)
        filename = self.finder.get_dividends_path(symbol, self.provider)

        if C.EX in df and C.DIV in df:
            df = self.reader.update_df(
                filename, df, C.EX).sort_values(by=[C.EX])
            df[C.DIV] = df[C.DIV].apply(lambda amt: float(amt) if amt else 0)

        return df

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

    def save_splits(self, **kwargs):
        # given a symbol, save its splits history
        symbol = kwargs['symbol']
        df = self.get_splits(**kwargs)
        self.writer.update_csv(
            self.finder.get_splits_path(symbol, self.provider), df)

# make tiingo OR IEX CLOUD!! version of get dividends which
# fetches existing dividend csv and adds a row if dividend
# today or fetches last 5 years, joins with existing and updates if new


class IEXCloud(MarketData):
    def __init__(self, broker=None):
        super().__init__(broker=broker)
        load_dotenv()
        self.base = 'https://cloud.iexapis.com'
        self.version = 'stable'
        self.token = os.environ['IEXCLOUD']
        self.provider = 'iexcloud'

    def get_endpoint(self, parts):
        # given a url
        # return an authenticated endpoint
        url = '/'.join(parts)
        endpoint = f'{url}?token={self.token}'
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
            # self.writer.save_json(f'data/{symbol}.json', data)
        else:
            print(f'Invalid response from IEX for {symbol} splits.')

        if not response.ok or data == []:
            return empty

        df = pd.DataFrame(data)

        return self.standardize_splits(symbol, df)


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
        pass
