import os
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
        # fee is 0.1%, so max spend_ratio is 99.9%
        fee = 0.001
        spend_ratio = spend_ratio - fee
        pair = f'{base}{quote}'
        side = side.upper()
        order_type = self.client.ORDER_TYPE_MARKET
        params = {'symbol': pair, 'type': order_type}
        symbol_info = self.client.get_symbol_info(pair)

        if side == 'SELL':
            side = self.client.SIDE_SELL
            balance_label = base
            quantity_label = 'quantity'
            filters = symbol_info['filters']
            for filter in filters:
                if filter['filterType'] == 'LOT_SIZE':
                    step_size = float(filter['stepSize'])
        elif side == 'BUY':
            side = self.client.SIDE_BUY
            balance_label = quote
            quantity_label = 'quoteOrderQty'
            precision = int(symbol_info['quoteAssetPrecision'])
        else:
            raise Exception('Need to specify BUY or SELL side for order')

        balance = float(self.client.get_asset_balance(balance_label)['free'])
        amount = spend_ratio * balance

        if side == 'BUY':
            quantity = "{:0.0{}f}".format(amount, precision)
        else:
            quantity = round_step_size(amount, step_size)

        params[quantity_label] = quantity

        params['side'] = side
        fx = self.client.create_order
        if test:
            fx = self.client.create_test_order

        order = fx(**params)
        return order

# write script that gets most recent data at 9pm est
# predicts using model
# writes that back to predict.csv
# write successful orders to binance.csv
