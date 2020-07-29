import sys
from multiprocessing import Pool
sys.path.append('src')
from DataSource import MarketData, BrokerData  # noqa autopep8
from FileOps import FileReader  # noqa autopep8

md = MarketData()
bd = BrokerData(None)
reader = FileReader()

symbols = md.get_symbols()


def save_dividend(symbol):
    try:
        bd.save_dividends(symbol)
    except:
        pass


with Pool() as p:
    p.map(save_dividend, symbols)
