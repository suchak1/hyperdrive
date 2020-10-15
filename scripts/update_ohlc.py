import sys
sys.path.append('src')
from DataSource import IEXCloud, Polygon  # noqa autopep8

iex = IEXCloud()
poly = Polygon()
symbols = iex.get_symbols()

# Double redundancy

for symbol in symbols:
    # 1st pass
    try:
        iex.save_ohlc(symbol=symbol, timeframe='1d')
    except Exception as e:
        print(f'IEX Cloud OHLC update failed for {symbol}.')
        print(e)

    # 2nd pass
    try:
        poly.save_ohlc(symbol=symbol, timeframe='1d')
    except Exception as e:
        print(f'Polygon.io OHLC update failed for {symbol}.')
        print(e)
