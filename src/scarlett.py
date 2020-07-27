import os
import json
import time
import pyotp
import robin_stocks as rh
from dotenv import load_dotenv
import pandas as pd
import yfinance as yf


# Classes:
# consider combining fileoperations into one class
# difference between broker and market data class?
# MAKE market data class (broker=None): if broker, then use broker.get_hist else use default get_hist (tiingo?)
# FileReader, FileWriter, DataSourcer, Utilities/Helper, Broker, Backtester, Strategy
# utils - move these to src/helpers.py and import *
# scarlett should have attrs broker, FileReader, engine, etc
# broker has subclasses robinhood, td ameritrade, ibkr


class FileReader:
    # file read operations

    def load_json(self, filename):
        # loads json file as dictionary data
        with open(filename, 'r') as file:
            return json.load(file)

    def load_csv(self, filename):
        # loads csv file as Dataframe
        try:
            df = pd.read_csv(filename)
        except pd.errors.EmptyDataError:
            # empty csv
            print(f'{filename} is an empty csv file.')
            df = pd.DataFrame()
        return df

    def check_update(self, filename, df):
        # given a csv filename and dataframe
        # return whether the csv needs to be updated
        return (not os.path.exists(filename)
                or len(self.load_csv(filename)) < len(df))


class FileWriter:
    # file write operations
    def save_json(self, filename, data):
        # saves data as json file with provided filename
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def save_csv(self, filename, data):
        # saves df as csv file with provided filename
        with open(filename, 'w') as f:
            data.to_csv(f, index=False)

    def update_csv(self, filename, df):
        # update csv if needed
        if FileReader().check_update(filename, df):
            self.save_csv(filename, df)


class Robinhood:
    # broker operation
    def __init__(self, usr=None, pwd=None, mfa=None):
        # Authentication
        load_dotenv()

        username = usr or os.environ['RH_USERNAME']
        password = pwd or os.environ['RH_PASSWORD']
        mfa_code = mfa or pyotp.TOTP(os.environ['RH_2FA']).now()

        rh.login(username, password, mfa_code=mfa_code)
        self.api = rh

    def get_symbols_from_instruments(self, instruments):
        # given a list of instruments,
        # return a list of corresponding symbols
        return [self.api.get_symbol_by_url(instrument)
                for instrument in instruments]

    def flatten(self, xxs):
        # flattens 2d list into 1d list
        return [x for xs in xxs for x in xs]

    def get_hists(self, symbols, span='year', interval='day', save=False):
        # given a list of symbols,
        # return a DataFrame with historical data
        hists = [self.api.get_stock_historicals(
            symbol, interval, span) for symbol in symbols]
        clean = [hist for hist in hists if hist != [None]]
        df = pd.DataFrame.from_records(self.flatten(clean))
        # look into diff b/w tz_localize and tz_convert w param 'US/Eastern'
        # ideally store utc time
        df['begins_at'] = pd.to_datetime(df['begins_at']).apply(
            lambda x: x.tz_localize(None))
        # df = df.sort_values('begins_at')
        if save is True:
            save_csv('data/data.csv', df)
        return df

    def get_names(self, symbols):
        # given a list of stock symbols
        # return a list of company names
        return [self.api.get_name_by_symbol(symbol)
                for symbol in symbols]

    def save_symbols(self):
        # save all the portfolio symbols in a table
        if not hasattr(self, 'symbols'):
            self.load_portfolio()
        symbols = list(self.symbols)
        names = self.get_names(symbols)
        df = pd.DataFrame({
            'symbol': symbols,
            'name': names
        })
        update_csv('data/symbols.csv', df)

    def load_portfolio(self):
        start = time.time()
        # Data acquisition
        self.positions = self.api.get_all_positions()
        self.holdings = self.api.build_holdings()
        # print(self.holdings)

        # Create lookup table instrument -> symbol and vice versa
        instruments = [position['instrument'] for position in self.positions]
        symbols = self.get_symbols_from_instruments(instruments)

        self.instruments = dict(zip(instruments, symbols))
        self.symbols = dict(map(reversed, self.instruments.items()))

        # Get historical data for all instruments
        self.hist = self.get_hists(symbols)
        end = time.time()
        print(f'Successfully loaded portfolio in {round(end-start, 2)}s.')


class MarketData:
    def get_dividends(self, symbol):
        # given a symbol,
        # return the dividend history
        ticker = yf.Ticker(symbol)
        return ticker.actions


class BrokerData(MarketData):
    def __init__(self, broker):
        self.broker = broker


class Scarlett:
    def __init__(self, load=False):

        self.broker = Robinhood()
        self.reader = FileReader()
        self.writer = FileWriter()

        if load is True:
            self.broker.load_portfolio()


# Scarlett(load=True).save_symbols()
