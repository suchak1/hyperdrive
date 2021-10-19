import os
import math
from pprint import pprint
from binance import Client
from binance.helpers import round_step_size
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('config.env'))


class Binance:
    def __init__(self, key=None, secret=None, testnet=False):
        load_dotenv(find_dotenv('config.env'))
        self.key = key
        self.secret = secret
        if not key:
            if testnet:
                self.key = os.environ['BINANCE_TESTNET_KEY']
            else:
                self.key = os.environ['BINANCE_KEY']
        if not secret:
            if testnet:
                self.secret = os.environ['BINANCE_TESTNET_SECRET']
            else:
                self.secret = os.environ['BINANCE_SECRET']
        self.client = Client(self.key, self.secret, testnet=testnet, tld='us')

    def order(self, base, quote, side, spend_ratio=1, test=False):
        pair = f'{base}{quote}'
        order_type = self.client.ORDER_TYPE_MARKET
        params = {'symbol': pair, 'type': order_type}
        symbol_info = self.client.get_symbol_info(pair)
        pprint(symbol_info)

        if side.lower() == 'sell':
            side = self.client.SIDE_SELL
            balance_label = base
            # precision_label = 'baseAssetPrecision'
            quantity_label = 'quantity'
            filters = symbol_info['filters']
            for filter in filters:
                if filter['filterType'] == 'LOT_SIZE':
                    precision = float(filter['stepSize'])
        else:
            side = self.client.SIDE_BUY
            balance_label = quote
            # precision_label = 'quoteAssetPrecision'
            quantity_label = 'quoteOrderQty'

        balance = float(self.client.get_asset_balance(balance_label)['free'])
        amount = spend_ratio * balance
        # precision = symbol_info[precision_label]
        # quantity = "{:0.0{}f}".format(amount, precision)
        # step_size = 0.0001
        quantity = round_step_size(amount, step_size)
        params[quantity_label] = quantity
        print(quantity_label, params[quantity_label])

        params['side'] = side
        fx = self.client.create_order
        if test:
            fx = self.client.create_test_order

        order = fx(**params)
        return order


#     order = client.order_market_buy(
#     symbol='BNBBTC',
#     quantity=100)

# order = client.order_market_sell(
#     symbol='BNBBTC',
#     quantity=100)
# buy
# sell
# get price
# write successful orders to binance.csv
