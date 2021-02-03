import sys
sys.path.append('src')
from Storage import Store  # noqa autopep8

store = Store()

# symbols = ['VTRS', 'IAC', 'CTVA', 'CARR', 'OTIS', 'HWM', 'GOOG']
if __name__ == '__main__':
    # for symbol in symbols:
    # store.upload_dir(path=f'data/intraday/polygon/{symbol}')
    store.upload_dir(path='data/intraday/polygon')
