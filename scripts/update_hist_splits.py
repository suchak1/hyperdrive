import os
import sys
from multiprocessing import Process
sys.path.append('src')
from DataSource import IEXCloud, Polygon  # noqa autopep8
from Constants import CI, PathFinder  # noqa autopep8


iex = IEXCloud()
poly = Polygon()
symbols = iex.get_symbols()
symbols = symbols[250:]

# Double redundancy

# 1st pass


def update_iex_splits():
    for symbol in symbols:
        filename = PathFinder().get_splits_path(
            symbol=symbol, provider=iex.provider)
        try:
            iex.save_splits(symbol=symbol, timeframe='5y')
        except Exception as e:
            print(f'IEX Cloud split update failed for {symbol}.')
            print(e)
        finally:
            if CI and os.path.exists(filename):
                os.remove(filename)
# 2nd pass


def update_poly_splits():
    for symbol in symbols:
        filename = PathFinder().get_splits_path(
            symbol=symbol, provider=poly.provider)
        try:
            poly.save_splits(symbol=symbol, timeframe='max')
        except Exception as e:
            print(f'Polygon.io split update failed for {symbol}.')
            print(e)
        finally:
            if CI and os.path.exists(filename):
                os.remove(filename)


p1 = Process(target=update_iex_splits)
p2 = Process(target=update_poly_splits)
p1.start()
p2.start()
p1.join()
p2.join()
