import os
import sys
import pandas as pd
sys.path.append('hyperdrive')
from DataSource import MarketData  # noqa autopep8
from History import Historian  # noqa autopep8
import Constants as C  # noqa autopep8

md = MarketData()
md.provider = 'polygon'
hist = Historian()

symbol = os.environ['SYMBOL']
signals_path = md.finder.get_signals_path()
signals = md.reader.load_csv(signals_path)
signals[C.TIME] = pd.to_datetime(signals[C.TIME])
df = md.get_ohlc(symbol).merge(signals, on=C.TIME)

holding_pf = hist.buy_and_hold(df[C.CLOSE])
hyper_pf = hist.create_portfolio(df[C.CLOSE], df[C.SIG], 0.001)

metrics = [
    'Total Return [%]',
    'Max Drawdown [%]',
    'Win Rate [%]',
    'Profit Factor',
    'Sharpe Ratio',
    'Sortino Ratio'
]

holding = {
    'balances': list(holding_pf.value()),
    'stats': dict(holding_pf.stats())
}
hyper = {
    'balances': list(hyper_pf.value()),
    'stats': dict(hyper_pf.stats())
}

holding_path = md.finder.get_api_path('holding')
hyper_path = md.finder.get_api_path('hyper')
md.writer.save_json(holding_path, holding)
md.writer.save_json(hyper_path, hyper)
