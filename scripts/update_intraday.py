import os
import sys
from multiprocessing import Process, Value
sys.path.append('hyperdrive')
from DataSource import Polygon  # noqa autopep8
from Constants import POLY_CRYPTO_SYMBOLS, FEW_DAYS  # noqa autopep8
import Constants as C  # noqa autopep8

counter = Value('i', 0)
poly = Polygon(os.environ['POLYGON'])
stock_symbols = poly.get_symbols()
crypto_symbols = POLY_CRYPTO_SYMBOLS
all_symbols = stock_symbols + crypto_symbols


def update_poly_intraday():
    for symbol in all_symbols:
        filenames = []
        try:
            filenames = poly.save_intraday(
                symbol=symbol, timeframe=FEW_DAYS, retries=1)
            with counter.get_lock():
                counter.value += 1
        except Exception as e:
            print(f'Polygon.io intraday update failed for {symbol}.')
            print(e)
        finally:
            if C.CI:
                for filename in filenames:
                    if os.path.exists(filename):
                        os.remove(filename)


p1 = Process(target=update_poly_intraday)
p1.start()
p1.join()

if counter.value / len(all_symbols) < 0.95:
    exit(1)
