import os
import json
import time
from pprint import pprint
import robin_stocks as rh
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt


# utils
def flatten(l):
    return [item for sublist in l for item in sublist]


def save_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


class Scarlett:
    def __init__(self, usr, pwd):
        # Authentication
        if usr and pwd:
            rh.login(usr, pwd)
        else:
            load_dotenv()
            rh.login(
                os.environ['EMAIL'],
                os.environ['PASSWORD'])
        self.rh = rh
        self.symbols = {}
        self.instruments = {}

    def get_symbols(self, instruments):
        # given a list of instruments,
        # return a list of corresponding symbols
        return [rh.stocks.get_symbol_by_url(instrument) for instrument in instruments]

    def get_hists(self, symbols, span='5year'):
        # given a list of symbols,
        # return a DataFrame with historical data
        hists = [self.rh.stocks.get_historicals(
            symbol, span) for symbol in symbols]
        clean = [hist for hist in hists if hist != [None]]
        df = pd.DataFrame.from_records(flatten(clean))
        df['begins_at'] = pd.to_datetime(df['begins_at'])
        # df = df.sort_values('begins_at')
        return df

    def load_portfolio(self):
        start = time.time()
        # Data acquisition
        self.positions = rh.account.get_all_positions()
        self.holdings = rh.build_holdings()

        # Create lookup table instrument -> symbol and vice versa
        instruments = [position['instrument'] for position in self.positions]
        symbols = self.get_symbols(instruments)

        self.instruments = dict(zip(instruments, symbols))
        self.symbols = dict(map(reversed, self.instruments.items()))

        # Get historical data for all instruments
        self.hist = self.get_hists(symbols)
        end = time.time()
        print(f'Successfully loaded portfolio in {round(end-start, 2)}s.')

    def plot(symbol, start=None, end=None, instrument=None):
        # given a stock symbol or instrument,
        # plot its historical price data

        # first, cache the symbol if we haven't loaded in its data
        # move this to an update function if we need to use it elsewhere
        if symbol not in self.symbols:
            instrument = self.rh.get_instruments_by_symbols(instrument)
            print(instrument)
            self.symbols[symbol] = instrument
            self.instruments[instrument] = symbol
            df = self.get_hists([instrument])
            if self.hist:
                self.hist = pd.concat([self.hist, df])
            else:
                self.hist = df

        # handle unset timeframe
        if not start:
            start = pd.Timestamp.min
        if not end:
            end = pd.Timestamp.max

        # then, plot the data
        df = self.hist[
            (self.hist['symbol'] == symbol) &
            (self.hist['begins_at'] <= start) &
            (self.hist['begins_at'] >= end)]
        df = df.sort_values('begins_at')
        plt.plot(df['begins_at'], df['close_price'])
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.title(f'{symbol} Stock Price')
        plt.show()

        # Scarlett()
