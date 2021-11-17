import os
import sys
from multiprocessing import Process, Value
sys.path.append('hyperdrive')
from DataSource import IEXCloud, Polygon  # noqa autopep8
import Constants as C  # noqa autopep8

counter = Value('i', 0)
iex = IEXCloud()
poly = Polygon()
symbols = iex.get_symbols()

# Double redundancy

# 1st pass


def update_iex_dividends():
    for symbol in symbols:
        try:
            filename = iex.save_dividends(
                symbol=symbol, timeframe='3m',
                retries=1 if C.TEST else C.DEFAULT_RETRIES)
            with counter.get_lock():
                counter.value += 1
            if C.CI and os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f'IEX Cloud dividend update failed for {symbol}.')
            print(e)

# 2nd pass


def update_poly_dividends():
    for symbol in symbols:
        try:
            filename = poly.save_dividends(symbol=symbol, timeframe='3m',
                                           retries=1 if C.TEST else C.DEFAULT_RETRIES)
            with counter.get_lock():
                counter.value += 1
            if C.CI and os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f'Polygon.io dividend update failed for {symbol}.')
            print(e)


p1 = Process(target=update_iex_dividends)
p2 = Process(target=update_poly_dividends)
p1.start()
p2.start()
p1.join()
p2.join()
