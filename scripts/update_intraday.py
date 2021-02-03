import os
import sys
from time import sleep
from multiprocessing import Process
sys.path.append('src')
from DataSource import IEXCloud, Polygon  # noqa autopep8
from Constants import PathFinder, POLY_CRYPTO_DELAY  # noqa autopep8
import Constants as C  # noqa autopep8

iex = IEXCloud()
poly_stocks = Polygon()
poly_crypto = Polygon(os.environ['POLYGON'])
stock_symbols = iex.get_symbols()
crypto_symbols = C.POLY_CRYPTO_SYMBOLS
few_days = '3d'

# Double redundancy

# 1st pass


def update_iex_intraday():
    for symbol in stock_symbols:
        filenames = []
        try:
            filenames = iex.save_intraday(
                symbol=symbol, timeframe='1d',
                retries=1 if C.TEST else C.DEFAULT_RETRIES)
        except Exception as e:
            print(f'IEX Cloud intraday update failed for {symbol}.')
            print(e)
        finally:
            if C.CI:
                for filename in filenames:
                    if os.path.exists(filename):
                        os.remove(filename)
# 2nd pass


def update_poly_stocks_intraday():
    for symbol in stock_symbols:
        filenames = []
        try:
            filenames = poly_stocks.save_intraday(
                symbol=symbol, timeframe=few_days,
                retries=1 if C.TEST else C.DEFAULT_RETRIES)
        except Exception as e:
            print(f'Polygon.io intraday update failed for {symbol}.')
            print(e)
        finally:
            if C.CI:
                for filename in filenames:
                    if os.path.exists(filename):
                        os.remove(filename)
# Crypto pass


def update_poly_crypto_intraday():
    for idx, symbol in enumerate(crypto_symbols):
        filenames = []
        try:
            filenames = poly_crypto.save_intraday(
                symbol=symbol, timeframe=few_days,
                retries=1 if C.TEST else C.DEFAULT_RETRIES)
        except Exception as e:
            print(f'Polygon.io intraday update failed for {symbol}.')
            print(e)
        finally:
            if C.CI:
                for filename in filenames:
                    if os.path.exists(filename):
                        os.remove(filename)

            if idx != len(crypto_symbols) - 1:
                sleep(POLY_CRYPTO_DELAY)


p1 = Process(target=update_iex_intraday)
p2 = Process(target=update_poly_stocks_intraday)
p3 = Process(target=update_poly_crypto_intraday)
p1.start()
p2.start()
p3.start()
