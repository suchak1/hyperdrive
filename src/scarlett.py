import os
import json
import time
# from pprint import pprint
import robin_stocks as rh
from dotenv import load_dotenv
import pandas as pd
import yfinance as yf


# utils - move these to src/helpers.py and import *
# scarlett should have attrs broker, datareader, engine, etc
# broker has subclasses robinhood, td ameritrade, ibkr
def flatten(xxs):
    # flattens 2d list into 1d list
    return [x for xs in xxs for x in xs]


def save_json(filename, data):
    # saves data as json file with provided filename
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def load_json(filename):
    # loads json file as dictionary data
    with open(filename, 'r') as file:
        return json.load(file)


def save_csv(filename, data):
    # saves df as csv file with provided filename
    with open(filename, 'w') as f:
        data.to_csv(f, index=False)


def check_update(filename, df):
    # given a csv filename and dataframe
    # return whether the csv needs to be updated
    return (not os.path.exists(filename)
            or len(load_csv(filename)) < len(df))


def update_csv(filename, df):
    # update csv if needed
    if check_update(filename, df):
        save_csv(filename, df)


def load_csv(filename):
    # loads csv file as Dataframe
    try:
        df = pd.read_csv(filename)
    except pd.errors.EmptyDataError:
        # empty csv
        print(f'{filename} is an empty csv file.')
        df = pd.DataFrame()
    return df


class Scarlett:
    def __init__(self, usr=None, pwd=None, load=False):
        # Authentication
        if usr and pwd:
            rh.login(usr, pwd)
        else:
            load_dotenv()
            rh.login(
                os.environ['EMAIL'],
                os.environ['PASSWORD'])
        self.rh = rh

        if load == True:
            self.load_portfolio()

    def get_symbols(self, instruments):
        # given a list of instruments,
        # return a list of corresponding symbols
        return [self.rh.get_symbol_by_url(instrument)
                for instrument in instruments]

    def get_hists(self, symbols, span='year'):
        # given a list of symbols,
        # return a DataFrame with historical data
        interval = 'day'
        hists = [self.rh.get_stock_historicals(
            symbol, interval, span) for symbol in symbols]
        clean = [hist for hist in hists if hist != [None]]
        df = pd.DataFrame.from_records(flatten(clean))
        # look into diff between tz_localize and tz_convert w param 'US/Eastern'
        # ideally store utc time
        df['begins_at'] = pd.to_datetime(df['begins_at']).apply(
            lambda x: x.tz_localize(None))
        # df = df.sort_values('begins_at')
        save_csv('data/data.csv', df)
        return df

    def get_dividends(self, symbol):
        # given a symbol,
        # return the dividend history
        ticker = yf.Ticker(symbol)
        return ticker.actions

    def get_names(self, symbols):
        # given a list of stock symbols
        # return a list of company names
        return [self.rh.get_name_by_symbol(symbol)
                for symbol in symbols]

    def save_symbols(self):
        # save all the portfolio symbols in a table
        if not hasattr(self, 'symbols'):
            self.load_portfolio()
        symbols = list(self.symbols)
        names = self.get_names(symbols)
        df = pd.DataFrame({
            'symbol': symbols,
            'names': names
        })
        update_csv('data/symbols.csv', df)

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


Scarlett(load=True).save_symbols()
