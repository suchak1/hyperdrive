import os
import sys
from multiprocessing import Process, Value
sys.path.append('hyperdrive')
from DataSource import IEXCloud, Polygon  # noqa autopep8
from Constants import POLY_CRYPTO_SYMBOLS, FEW_DAYS  # noqa autopep8
import Constants as C  # noqa autopep8

counter = Value('i', 0)
iex = IEXCloud()
poly = Polygon(os.environ['POLYGON'])
stock_symbols = iex.get_symbols()
crypto_symbols = POLY_CRYPTO_SYMBOLS
all_symbols = stock_symbols + crypto_symbols

# Double redundancy

# 1st pass


def update_iex_ohlc():
    for symbol in stock_symbols:
        try:
            filename = iex.save_ohlc(
                symbol=symbol, timeframe='1d',
                retries=1 if C.TEST else C.DEFAULT_RETRIES)
            with counter.get_lock():
                counter.value += 1
            if C.CI and os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f'IEX Cloud OHLC update failed for {symbol}.')
            print(e)

# 2nd pass


def update_poly_ohlc():
    for symbol in all_symbols:
        try:
            filename = poly.save_ohlc(
                symbol=symbol, timeframe=FEW_DAYS, retries=1)
            with counter.get_lock():
                counter.value += 1
            if C.CI and os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f'Polygon.io OHLC update failed for {symbol}.')
            print(e)


p1 = Process(target=update_iex_ohlc)
p2 = Process(target=update_poly_ohlc)
p1.start()
p2.start()
p1.join()
p2.join()

if counter / (len(stock_symbols) + len(all_symbols)) < 0.95:
    exit(1)
