import os
import sys
from time import sleep
from multiprocessing import Process
sys.path.append('src')
from DataSource import IEXCloud, Polygon  # noqa autopep8
from Constants import CI, PathFinder, POLY_CRYPTO_SYMBOLS  # noqa autopep8


iex = IEXCloud()
poly_stocks = Polygon()
poly_crypto = Polygon(os.environ['POLYGON'])
stock_symbols = iex.get_symbols()[250:]
crypto_symbols = POLY_CRYPTO_SYMBOLS
# Double redundancy

# 1st pass


def update_iex_ohlc():
    for symbol in stock_symbols:
        filename = PathFinder().get_ohlc_path(
            symbol=symbol, provider=iex.provider)
        if os.path.exists(filename):
            os.remove(filename)
        try:
            iex.save_ohlc(symbol=symbol, timeframe='max')
        except Exception as e:
            print(f'IEX Cloud OHLC update failed for {symbol}.')
            print(e)
        finally:
            if CI and os.path.exists(filename):
                os.remove(filename)
# 2nd pass


def update_poly_stocks_ohlc():
    for symbol in stock_symbols:
        filename = PathFinder().get_ohlc_path(
            symbol=symbol, provider=poly_stocks.provider)
        if os.path.exists(filename):
            os.remove(filename)
        try:
            poly_stocks.save_ohlc(symbol=symbol, timeframe='max')
        except Exception as e:
            print(f'Polygon.io OHLC update failed for {symbol}.')
            print(e)
        finally:
            if CI and os.path.exists(filename):
                os.remove(filename)
# Crypto pass


def update_poly_crypto_ohlc():
    calls_per_min = 5
    for idx, symbol in enumerate(crypto_symbols):
        filename = PathFinder().get_ohlc_path(
            symbol=symbol, provider=poly_crypto.provider)
        if os.path.exists(filename):
            os.remove(filename)
        try:
            poly_crypto.save_ohlc(symbol=symbol, timeframe='max')
        except Exception as e:
            print(f'Polygon.io OHLC update failed for {symbol}.')
            print(e)
        finally:
            if CI and os.path.exists(filename):
                os.remove(filename)

            if idx != len(crypto_symbols) - 1:
                sleep(60 // calls_per_min + 5)


p1 = Process(target=update_iex_ohlc)
p2 = Process(target=update_poly_stocks_ohlc)
p3 = Process(target=update_poly_crypto_ohlc)
p1.start()
p2.start()
p3.start()
