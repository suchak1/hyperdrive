import os
import json
import time
# from pprint import pprint
import robin_stocks as rh
from dotenv import load_dotenv
import pandas as pd


# utils
def flatten(xxs):
    # flattens 2d list into 1d list
    return [x for xs in xxs for x in xs]


def save_file(filename, data):
    # saves data as json file with provided filename
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def load_file(filename):
    # loads json file as dictionary data
    with open(filename, 'r') as file:
        return json.load(file)


class Scarlett:
    def __init__(self, usr=None, pwd=None):
        # Authentication
        if usr and pwd:
            rh.login(usr, pwd)
        else:
            load_dotenv()
            rh.login(
                os.environ['EMAIL'],
                os.environ['PASSWORD'])
        self.rh = rh

    def get_symbols(self, instruments):
        # given a list of instruments,
        # return a list of corresponding symbols
        return [self.rh.get_symbol_by_url(instrument)
                for instrument in instruments]

    def get_hists(self, symbols, span='5year'):
        # given a list of symbols,
        # return a DataFrame with historical data
        hists = [self.rh.get_stock_historicals(
            symbol, span) for symbol in symbols]
        clean = [hist for hist in hists if hist != [None]]
        df = pd.DataFrame.from_records(flatten(clean))
        # look into diff between tz_localize and tz_convert w param 'US/Eastern'
        # ideally store utc time
        df['begins_at'] = pd.to_datetime(df['begins_at']).apply(
            lambda x: x.tz_localize(None))
        # df = df.sort_values('begins_at')
        return df

    def load_portfolio(self):
        start = time.time()
        # Data acquisition
        self.positions = self.rh.get_all_positions()
        self.holdings = self.rh.build_holdings()

        # Create lookup table instrument -> symbol and vice versa
        instruments = [position['instrument'] for position in self.positions]
        symbols = self.get_symbols(instruments)

        self.instruments = dict(zip(instruments, symbols))
        self.symbols = dict(map(reversed, self.instruments.items()))

        # Get historical data for all instruments
        self.hist = self.get_hists(symbols)
        end = time.time()
        print(f'Successfully loaded portfolio in {round(end-start, 2)}s.')

# Scarlett()
