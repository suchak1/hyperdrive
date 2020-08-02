import os
import requests
import pandas as pd
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

    def get_symbols(self):
        # get cached list of symbols
        symbols_path = self.finder.get_symbols_path()
        return list(self.reader.load_csv(symbols_path)['symbol'])

    def get_dividends(self, symbol):
        # given a symbol, return a cached dataframe
        return self.reader.load_csv(self.finder.get_dividends_path(symbol))

    def save_dividends(self, symbol):
        # given a symbol, save its dividend history
        df = self.get_dividends(symbol)
        self.writer.update_csv(f'data/dividends/{symbol.upper()}.csv', df)

    # def save_splits(self, symbol):
    #     # given a symbol, save its stock split history
    #     df = self.get_splits(symbol)
    #     self.writer.update_csv(f'data/splits/{symbol.upper()}.csv', df)

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
            symbol,
            dataset,
            timeframe
        ]
        endpoint = self.get_endpoint(parts)
        response = requests.get(endpoint)
        empty = pd.DataFrame()

        if response.ok:
            data = [datum for datum in response.json() if datum['flag']
                    == 'Cash' and datum['currency'] == 'USD']
            self.writer.save_json(f'data/{symbol}.json', data)
        else:
            print(f'Invalid response from IEX for {symbol} dividends.')

        if not response or data == []:
            return empty

        columns = ['exDate', 'paymentDate', 'declaredDate', 'amount']
        mapping = dict(zip(columns, [C.EX, C.PAY, C.DEC, C.DIV]))
        df = pd.DataFrame(data)[columns].rename(columns=mapping)

        filename = self.finder.get_dividends_path(symbol)

        df = self.reader.update_df(filename, df, C.EX).sort_values(by=[C.EX])
        df[C.DIV] = df[C.DIV].apply(lambda amt: float(amt) if amt else 0)

        return df

    # def get_splits(self, symbol):
    #     # given a symbol, return the stock splits
    #     ticker = yf.Ticker(symbol.replace('.', '-'))
    #     df = ticker.actions.reset_index().drop(
    #         'Dividends',
    #         axis=1
    #     )
    #     df = df[df['Stock Splits'] != 0]
    #     return df
