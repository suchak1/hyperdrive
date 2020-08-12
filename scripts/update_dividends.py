import sys
from multiprocessing import Pool
sys.path.append('src')
from DataSource import IEXCloud  # noqa autopep8


iex = IEXCloud()
symbols = iex.get_symbols()


def multi_div(symbol):
    # define fx to be pickled in multiprocessing
    iex.save_dividends(symbol)


# save files as CSVs and uploads to S3
with Pool() as p:
    p.map(multi_div, symbols)
