import os
import sys
from time import sleep
from multiprocessing import Process
sys.path.append('src')
from DataSource import IEXCloud, Polygon  # noqa autopep8
from Constants import PathFinder  # noqa autopep8
import Constants as C  # noqa autopep8

iex = IEXCloud()
poly_stocks = Polygon()
poly_crypto = Polygon(os.environ['POLYGON'])
stock_symbols = iex.get_symbols()
crypto_symbols = C.POLY_CRYPTO_SYMBOLS
yesterday = iex.traveller.dates_in_range('1d')[0]
# Double redundancy

# 1st pass


def update_iex_intraday():
    for symbol in stock_symbols:
        try:
            iex.save_intraday(symbol=symbol, timeframe='1d',
                              retries=1 if C.TEST else C.DEFAULT_RETRIES)
        except Exception as e:
            print(f'IEX Cloud intraday update failed for {symbol}.')
            print(e)
        finally:
            filename = PathFinder().get_intraday_path(
                symbol=symbol,
                date=yesterday,
                provider=iex.provider)
            if C.CI and os.path.exists(filename):
                os.remove(filename)
# 2nd pass


def update_poly_stocks_intraday():
    for symbol in stock_symbols:
        try:
            poly_stocks.save_intraday(
                symbol=symbol, timeframe='1d',
                retries=1 if C.TEST else C.DEFAULT_RETRIES)
        except Exception as e:
            print(f'Polygon.io intraday update failed for {symbol}.')
            print(e)
        finally:
            filename = PathFinder().get_intraday_path(
                symbol=symbol,
                date=yesterday,
                provider=poly_stocks.provider)
            if C.CI and os.path.exists(filename):
                os.remove(filename)
# Crypto pass


def update_poly_crypto_intraday():
    calls_per_min = 5
    for idx, symbol in enumerate(crypto_symbols):
        try:
            poly_crypto.save_intraday(symbol=symbol, timeframe='1d',
                                      retries=1 if C.TEST else C.DEFAULT_RETRIES)
        except Exception as e:
            print(f'Polygon.io intraday update failed for {symbol}.')
            print(e)
        finally:
            filename = PathFinder().get_intraday_path(
                symbol=symbol,
                date=yesterday,
                provider=poly_crypto.provider)
            if C.CI and os.path.exists(filename):
                os.remove(filename)

            if idx != len(crypto_symbols) - 1:
                sleep(60 // calls_per_min + 5)


p1 = Process(target=update_iex_intraday)
p2 = Process(target=update_poly_stocks_intraday)
p3 = Process(target=update_poly_crypto_intraday)
p1.start()
p2.start()
p3.start()
