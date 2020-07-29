import sys
from multiprocessing import Pool
sys.path.append('src')
from DataSource import BrokerData  # noqa autopep8
from FileOps import FileReader  # noqa autopep8

bd = BrokerData(None)
reader = FileReader()

symbols = list(reader.load_csv('data/symbols.csv')['symbol'])


def save_dividend(symbol):
    try:
        bd.save_dividends(symbol)
    except:
        pass


with Pool() as p:
    p.map(save_dividend, symbols)
