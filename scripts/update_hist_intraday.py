import os
import sys
from time import sleep
from datetime import datetime
from multiprocessing import Process
sys.path.append('src')
from DataSource import IEXCloud, Polygon  # noqa autopep8
from Constants import CI, PathFinder, POLY_CRYPTO_SYMBOLS, POLY_CRYPTO_DELAY  # noqa autopep8


poly_stocks = Polygon()
poly_crypto = Polygon(os.environ['POLYGON'])
stock_symbols = poly_stocks.get_symbols()
last_completed_stock = 'NVDA'
stock_symbols = stock_symbols[stock_symbols.index(last_completed_stock)+1:]
# [250:]
crypto_symbols = POLY_CRYPTO_SYMBOLS


def update_poly_stocks_intraday():
    for symbol in stock_symbols:
        now = datetime.now()
        hour = now.hour
        while hour in set(range(9, 12)):
            print(now.strftime('%H:%M'))
            print('Sleeping for 1 hr')
            sleep(3600)
            hour = datetime.now().hour
        filenames = []
        try:
            filenames = poly_stocks.save_intraday(
                symbol=symbol, timeframe='7700d', retries=1)
        except Exception as e:
            print(f'Polygon.io intraday update failed for {symbol}.')
            print(e)
        finally:
            if CI:
                for filename in filenames:
                    if os.path.exists(filename):
                        os.remove(filename)
# Crypto pass


def update_poly_crypto_intraday():

    for idx, symbol in enumerate(crypto_symbols):
        filenames = []
        try:
            filenames = poly_crypto.save_intraday(
                symbol=symbol, timeframe='9m',
                delay=POLY_CRYPTO_DELAY, retries=2)
        except Exception as e:
            print(f'Polygon.io intraday update failed for {symbol}.')
            print(e)
        finally:
            if CI:
                for filename in filenames:
                    if os.path.exists(filename):
                        os.remove(filename)

            if idx != len(crypto_symbols) - 1:
                sleep(POLY_CRYPTO_DELAY)


p2 = Process(target=update_poly_stocks_intraday)
# p3 = Process(target=update_poly_crypto_intraday)
p2.start()
# p3.start()
