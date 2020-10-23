import sys
from multiprocessing import Process
sys.path.append('src')
from DataSource import IEXCloud, Polygon  # noqa autopep8

iex = IEXCloud()
poly = Polygon()
symbols = iex.get_symbols()
symbols = symbols[250:]

# Double redundancy

# 1st pass


def update_iex_splits():
    for symbol in symbols:
        try:
            iex.save_splits(symbol=symbol, timeframe='5y')
        except Exception as e:
            print(f'IEX Cloud split update failed for {symbol}.')
            print(e)
# 2nd pass


def update_poly_splits():
    for symbol in symbols:
        try:
            poly.save_splits(symbol=symbol, timeframe='max')
        except Exception as e:
            print(f'Polygon.io split update failed for {symbol}.')
            print(e)


p1 = Process(target=update_iex_splits)
p2 = Process(target=update_poly_splits)
p1.start()
p2.start()
