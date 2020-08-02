import sys
from multiprocessing import Pool
sys.path.append('src')
from DataSource import IEXCloud  # noqa autopep8


iex = IEXCloud()
symbols = iex.get_symbols()
# symbols = ['NTDOY']


def multi_div(symbol):
    iex.save_dividends(symbol)


with Pool() as p:
    p.map(multi_div, symbols)
