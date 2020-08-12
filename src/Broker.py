import os
import time
import pyotp
import robin_stocks as rh
from dotenv import load_dotenv
import pandas as pd
from Constants import PathFinder
import Constants as C
from FileOps import FileReader, FileWriter

# broker has subclasses robinhood, td ameritrade, ibkr


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
        self.writer = FileWriter()
        self.reader = FileReader()
        self.finder = PathFinder()

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
            self.writer.save_csv('data/data.csv', df)
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
            C.SYMBOL: symbols,
            C.NAME: names
        })
        self.writer.update_csv(self.finder.get_symbols_path(), df)

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
