import json
from pprint import pprint
import os
import sys
import pandas as pd
import vectorbt as vbt
sys.path.append('hyperdrive')
from DataSource import MarketData  # noqa autopep8
from History import Historian  # noqa autopep8
import Constants as C  # noqa autopep8

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


md = MarketData()
md.provider = 'polygon'
hist = Historian()

symbol = os.environ['SYMBOL']
signals_path = md.finder.get_signals_path()
signals = md.reader.load_csv(signals_path)
signals[C.TIME] = pd.to_datetime(signals[C.TIME])
df = md.get_ohlc(symbol).merge(signals, on=C.TIME)

# 1 week delay
df = df.head(len(df) - 5)
close = df[C.CLOSE]


def create_portfolio_preview(close, signals, init_cash):
    holding_pf = hist.buy_and_hold(close, init_cash)
    holding_pf =
    hyper_pf = hist.create_portfolio(close, signals, init_cash, 0.001)

    holding_balances = [round(bal, 2) for bal in list(holding_pf.value())]
    hyper_balances = [round(bal, 2) for bal in list(hyper_pf.value())]

    holding_stats = transform_stats(holding_pf.stats())
    # holding_stats['']
    hyper_stats = transform_stats(hyper_pf.stats())

    dates = list(df[C.TIME].dt.strftime('%m/%d/%Y'))
    signals = hist.unfill(list(df[C.SIG]))
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
    return preview


usd_preview = create_portfolio_preview(close, df[C.SIG], close.iloc[0])
btc_preview = create_portfolio_preview(
    1 / close, ~df[C.SIG], 1 + vbt.utils.math.abs_tol)
pprint(usd_preview)
pprint(btc_preview)
with open('preview2.json', 'w') as file:
    json.dump(btc_preview, file, indent=4)
# preview_path = md.finder.get_api_path('preview')
# md.writer.save_json(preview_path, preview)
