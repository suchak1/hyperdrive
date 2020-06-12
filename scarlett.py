import os
import json
from pprint import pprint
import robin_stocks as rh
from dotenv import load_dotenv

class Scarlett:
    def __init__(self):
        # Authentication
        load_dotenv()
        rh.login(
            os.environ['EMAIL'], 
            os.environ['PASSWORD'])
        
        # Data acquisition
        positions = rh.account.get_all_positions()
        holdings = rh.build_holdings()
        # need to get historicals for all instruments in positions
        # need to create instrument symbol lookup table

Scarlett()