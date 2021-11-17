import os
import sys
from multiprocessing import Process, Value
sys.path.append('hyperdrive')
from DataSource import IEXCloud, Polygon  # noqa autopep8
from Constants import PathFinder  # noqa autopep8
import Constants as C  # noqa autopep8

counter = Value('i', 0)
iex = IEXCloud()
poly = Polygon()
symbols = iex.get_symbols()

# Double redundancy

# 1st pass


def update_iex_splits():
    for symbol in symbols:
        try:
            filename = iex.save_splits(
                symbol=symbol, timeframe='3m',
                retries=1 if C.TEST else C.DEFAULT_RETRIES)
            with counter.get_lock():
                counter.value += 1
            if C.CI and os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f'IEX Cloud split update failed for {symbol}.')
            print(e)

# 2nd pass


def update_poly_splits():
    for symbol in symbols:
        try:
            filename = poly.save_splits(
                symbol=symbol, timeframe='3m',
                retries=1 if C.TEST else C.DEFAULT_RETRIES)
            with counter.get_lock():
                counter.value += 1
            if C.CI and os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f'Polygon.io split update failed for {symbol}.')
            print(e)


p1 = Process(target=update_iex_splits)
p2 = Process(target=update_poly_splits)
p1.start()
p2.start()
p1.join()
p2.join()

if counter.value / (len(symbols) * 2) < 0.95:
    exit(1)
