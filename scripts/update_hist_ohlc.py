import os
import sys
from multiprocessing import Process
sys.path.append('hyperdrive')
from DataSource import Polygon  # noqa autopep8
from Constants import CI, PathFinder, POLY_CRYPTO_SYMBOLS  # noqa autopep8


poly = Polygon(os.environ['POLYGON'])
stock_symbols = poly.get_symbols()
crypto_symbols = POLY_CRYPTO_SYMBOLS
all_symbols = stock_symbols + crypto_symbols
timeframe = '2m'


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


p1 = Process(target=update_poly_ohlc)
p1.start()
p1.join()
