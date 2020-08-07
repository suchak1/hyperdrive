import sys
from multiprocessing import Pool
sys.path.append('src')
from DataSource import IEXCloud  # noqa autopep8
from Storage import Store  # noqa autopep8
import Constants as C  # noqa autopep8


iex = IEXCloud()
symbols = iex.get_symbols()


def multi_div(symbol):
    # define fx to be pickled in multiprocessing
    iex.save_dividends(symbol)


# save files as CSVs
with Pool() as p:
    p.map(multi_div, symbols)

# upload dividend data to S3
Store().upload_dir(C.FULL_DIV_DIR)
