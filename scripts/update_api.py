import os
import sys
import json
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

# 1 week delay
df = df.head(len(df) - 7)

holding_pf = hist.buy_and_hold(df[C.CLOSE])
hyper_pf = hist.create_portfolio(df[C.CLOSE], df[C.SIG], 0.001)

holding_balances = list(holding_pf.value())
hyper_balances = list(hyper_pf.value())

metrics = [
    'Total Return [%]',
    'Max Drawdown [%]',
    'Win Rate [%]',
    'Profit Factor',
    'Sharpe Ratio',
    'Sortino Ratio'
]


def transform_stats(stats):
    return {
        k: (
            None if pd.isna(v) else round(v, 2)
        ) for k, v in dict(stats[metrics]).items()
    }


holding_stats = transform_stats(holding_pf.stats())
hyper_stats = transform_stats(hyper_pf.stats())


dates = list(df[C.TIME].dt.strftime('%m/%d/%Y'))
signals = list(df[C.SIG])
records = []

for idx, date in enumerate(dates):
    records.append({
        'Name': 'HODL',
        C.TIME: date,
        C.BAL: holding_balances[idx],
    })

    records.append({
        'Name': 'hyperdrive',
        C.TIME: date,
        C.BAL: hyper_balances[idx],
        C.SIG: signals[idx]
    })

stats = []
for idx, metric in enumerate(metrics):

    stats.append({
        'key': idx,
        'metric': metric,
        'HODL': holding_stats[metric],
        'hyperdrive': hyper_stats[metric]
    })


preview = {
    'data': records,
    'stats': stats
}

preview_path = md.finder.get_api_path('preview')
md.writer.save_json(preview_path, preview)
