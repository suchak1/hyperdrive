import sys
sys.path.append('src')
from Broker import Robinhood  # noqa autopep8

broker = Robinhood()
broker.load_portfolio()
broker.save_symbols()
