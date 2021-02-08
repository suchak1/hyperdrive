import sys
sys.path.append('src')
from Storage import Store  # noqa autopep8
from DataSource import Polygon  # noqa autopep8


store = Store()
poly = Polygon()


# to_download = ['DOW', 'DUK', 'FOX',
#                'GD', 'GE', 'GILD', 'GLD', 'GM']
to_download = ['HD', 'INSG']

# s3://hyperdrive.pro/data/intraday/polygon/
symbols = ['IBM', 'ICLN', 'INO', 'INTC',
           'IPO', 'IQ', 'ISRG']
# F, G, H, I
if __name__ == '__main__':
    for symbol in symbols:
        store.upload_dir(path=f'data/intraday/polygon/{symbol}')
        poly.save_intraday(
            symbol=symbol,
            timeframe='30d',
            retries=1
        )
    for symbol in to_download:
        poly.save_intraday(
            symbol=symbol,
            timeframe='6250d',
            retries=1
        )
