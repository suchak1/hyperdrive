import sys
import pandas as pd
from datetime import datetime, timedelta
sys.path.append('hyperdrive')
from DataSource import MarketData  # noqa
from Exchange import Binance  # noqa autopep8
import Constants as C  # noqa

bn = Binance()
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
    base = 'BTC'
    quote = 'USD'

    order = bn.order(base, quote, 'BUY' if signal else 'SELL')
    order_df = pd.json_normalize(order)

    yesterday = (
        datetime.utcnow().date() -
        timedelta(days=1)
    ).strftime(C.DATE_FMT)
    order_df[C.TIME] = [yesterday]

    orders = md.reader.update_df(orders_path, order_df, C.TIME, C.DATE_FMT)
    md.writer.update_csv(orders_path, orders)
