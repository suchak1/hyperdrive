import sys
sys.path.append('src')
from DataSource import BrokerData  # noqa autopep8
from FileOps import FileReader  # noqa autopep8

bd = BrokerData(None)
reader = FileReader()

symbols = list(reader.load_csv('data/symbols.csv')['symbol'])

for symbol in symbols:
    try:
        bd.save_dividends(symbol)
    except:
        pass
