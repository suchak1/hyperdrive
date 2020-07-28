import sys
sys.path.append('src')
from Broker import Robinhood  # noqa autopep8
from DataSource import BrokerData  # noqa autopep8

broker = Robinhood()
bd = BrokerData(None)
# symbols = get all symbols here and iterate
bd.save_dividends('AAPL')
