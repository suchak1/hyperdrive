import os
import sys
from multiprocessing import Process
sys.path.append('src')
from DataSource import IEXCloud, Polygon  # noqa autopep8
from Constants import CI, PathFinder, POLY_CRYPTO_SYMBOLS  # noqa autopep8


iex = IEXCloud()
poly = Polygon(os.environ['POLYGON'])
stock_symbols = iex.get_symbols()
crypto_symbols = POLY_CRYPTO_SYMBOLS
all_symbols = stock_symbols + crypto_symbols
timeframe = '2m'
# Double redundancy

# 1st pass


def update_iex_ohlc():
    for symbol in stock_symbols:
        filename = PathFinder().get_ohlc_path(
            symbol=symbol, provider=iex.provider)
        try:
            iex.save_ohlc(symbol=symbol, timeframe=timeframe)
        except Exception as e:
            print(f'IEX Cloud OHLC update failed for {symbol}.')
            print(e)
        finally:
            if CI and os.path.exists(filename):
                os.remove(filename)
# 2nd pass


def update_poly_ohlc():
    for symbol in all_symbols:
        filename = PathFinder().get_ohlc_path(
            symbol=symbol, provider=poly.provider)
        try:
            poly.save_ohlc(symbol=symbol, timeframe=timeframe)
        except Exception as e:
            print(f'Polygon.io OHLC update failed for {symbol}.')
            print(e)
        finally:
            if CI and os.path.exists(filename):
                os.remove(filename)


p1 = Process(target=update_iex_ohlc)
p2 = Process(target=update_poly_ohlc)
p1.start()
p2.start()
p1.join()
p2.join()
