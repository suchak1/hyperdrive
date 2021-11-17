import sys
sys.path.append('hyperdrive')
from Broker import Robinhood  # noqa autopep8

broker = Robinhood()
broker.save_symbols()
