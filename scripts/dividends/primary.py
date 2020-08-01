import sys
from multiprocessing import Pool
sys.path.append('src')
from DataSource import BrokerData  # noqa autopep8


bd = BrokerData(None)
symbols = bd.get_symbols()


def multi_div(symbol):
    try:
        bd.save_dividends(symbol)
    except:
        pass


with Pool() as p:
    p.map(multi_div, symbols)
