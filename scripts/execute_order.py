import sys
import pandas as pd
from datetime import datetime, timedelta
sys.path.append('hyperdrive')
from DataSource import MarketData  # noqa
from Exchange import Binance, Kraken  # noqa autopep8
import Constants as C  # noqa

test = C.TEST or C.DEV

bn = Binance(testnet=test)
kr = Kraken(test=test)
md = MarketData()
md.provider = 'polygon'

signals_path = md.finder.get_signals_path()
orders_path = md.finder.get_orders_path()

signals_df = md.reader.load_csv(signals_path)
last_two_signals = signals_df[C.SIG].tail(2).to_numpy()
num_unique_signals = len(set(last_two_signals))
signal = last_two_signals[-1]
should_order = num_unique_signals > 1

if should_order:
    side = C.BUY if signal else C.SELL
    if C.PREF_EXCHANGE == C.BINANCE:
        base = 'BTC'
        quote = 'USDT' if test else 'USD'
        spend_ratio = 0.01 if test else 1

        order = bn.order(base, quote, side, spend_ratio, test)
        order['exchange'] = C.BINANCE
    else:
        base = 'XXBT'
        quote = 'ZUSD'
        spend_ratio = 0.0005 if test else 1

        order = kr.order(base, quote, side, spend_ratio, test)
        if not test:
            trades = kr.get_trades(order['trades'])
            order = kr.standardize_order(order, trades)
        order['exchange'] = C.KRAKEN

    order_df = pd.json_normalize(order)

    yesterday = (
        datetime.utcnow().date() -
        timedelta(days=1)
    ).strftime(C.DATE_FMT)
    order_df[C.TIME] = [yesterday]

    orders = md.reader.update_df(orders_path, order_df, C.TIME, C.DATE_FMT)
    md.writer.update_csv(orders_path, orders)
