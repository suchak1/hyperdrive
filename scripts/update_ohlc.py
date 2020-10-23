import sys
from multiprocessing import Process
sys.path.append('src')
from DataSource import IEXCloud, Polygon  # noqa autopep8

iex = IEXCloud()
poly = Polygon()
symbols = iex.get_symbols()

# Double redundancy

# 1st pass


def update_iex_ohlc():
    for symbol in symbols:
        try:
            iex.save_ohlc(symbol=symbol, timeframe='1d')
        except Exception as e:
            print(f'IEX Cloud OHLC update failed for {symbol}.')
            print(e)
# 2nd pass


def update_poly_ohlc():
    for symbol in symbols:
        try:
            poly.save_ohlc(symbol=symbol, timeframe='1d')
        except Exception as e:
            print(f'Polygon.io OHLC update failed for {symbol}.')
            print(e)


p1 = Process(target=update_iex_ohlc)
p2 = Process(target=update_poly_ohlc)
p1.start()
p2.start()
