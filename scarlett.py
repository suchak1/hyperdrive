import os
# import json
# from pprint import pprint
import robin_stocks as rh
from dotenv import load_dotenv
import time

class Scarlett:
    def __new__(cls, *args, **kwargs):
        start = time.time()
        # Authentication
        if len(args) > 2:
            raise Exception("Too many arguments. Only need email and password or store your credentials under environment variables 'EMAIL' and 'PASSWORD'.")
        
        if usr and pwd:
            rh.login(usr, pwd)
        else:
            load_dotenv()
            rh.login(
                os.environ['EMAIL'], 
                os.environ['PASSWORD'])
        
        # Data acquisition
        positions = rh.account.get_all_positions()
        holdings = rh.build_holdings()
        # need to get historicals for all instruments in positions
        instruments = {}
        for position in positions:
            instrument = position['instrument']
            symbol = rh.stocks.get_symbol_by_url(position['instrument'])
            instruments[instrument] = symbol
        symbols = dict(map(reversed, instruments.items()))
        
        end = time.time()
        print(f'Successfully loaded portfolio in {round(end-start, 2)}s.')
        return self
    def load_portfolio

# Scarlett()