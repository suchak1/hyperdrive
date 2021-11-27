import os
import sys
sys.path.append('hyperdrive')
from DataSource import MarketData  # noqa autopep8
from History import Historian  # noqa autopep8
import Constants as C  # noqa autopep8

# run this script after ohlc (maybe during intra update)

md = MarketData()

symbol = os.environ['SYMBOL']
signals_path = md.finder.get_signals_path()
signals = md.reader.load_csv(signals_path)
df = md.get_ohlc(symbol).merge(signals, on=C.TIME)


md.writer.save_json('data/api/holding.json', holding)
md.writer.save_json('data/api/hyper.json', hyper)
