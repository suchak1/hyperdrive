import os
import time
import hmac
import base64
import hashlib
import requests
import urllib.parse
from binance import Client
from binance.helpers import round_step_size
from dotenv import load_dotenv, find_dotenv
import Constants as C
load_dotenv(find_dotenv('config.env'))


class CEX:
    def create_pair(self, base, quote):
        return f'{base}{quote}'


class Kraken(CEX):
    def __init__(self, key=None, secret=None, test=False):
        super().__init__()
        self.key = key
        self.secret = secret
        self.test = test
        if not key:
            self.key = os.environ['KRAKEN_KEY']
        if not secret:
            self.secret = os.environ['KRAKEN_SECRET']
        self.api_url = 'https://api.kraken.com'
        self.version = '0'

    def get_signature(self, urlpath, data):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def make_auth_req(self, uri_path, data):
        headers = {}
        headers['API-Key'] = self.key
        # get_kraken_signature() as defined in the 'Authentication' section
        headers['API-Sign'] = self.get_signature(uri_path, data)
        response = requests.post(
            (self.api_url + uri_path),
            headers=headers,
            data=data
        )
        return self.handle_response(response)

    def gen_nonce(self):
        return str(int(1000 * time.time()))

    def get_balance(self):
        access = 'private'
        endpoint = 'Balance'
        parts = [
            '',
            self.version,
            access,
            endpoint,
        ]
        url = '/'.join(parts)
        data = {
            "nonce": self.gen_nonce()
        }
        response = self.make_auth_req(url, data)
        return response

    def get_asset_pair(self, pair):
        access = 'public'
        endpoint = 'AssetPairs'
        parts = [
            self.api_url,
            self.version,
            access,
            endpoint,
        ]
        url = '/'.join(parts)
        params = {'pair': pair}
        response = requests.get(url, params=params)
        result = self.handle_response(response)[pair]
        return result

    def order(self, base, quote, side, spend_ratio=1, test=False):
        pair = self.create_pair(base, quote)
        pair_info = self.get_asset_pair(pair)
        # uncomment this to account for fees
        # fee = pair_info['fees'][0][1] / 100
        # uncomment this to account for fees
        spend_ratio = spend_ratio  # - fee
        side = side.lower()
        access = 'private'
        endpoint = 'AddOrder'
        parts = [
            '',
            self.version,
            access,
            endpoint,
        ]
        url = '/'.join(parts)

        oflags = ['nompp']
        balance_label = base
        precision_label = 'lot_decimals'

        if side.upper() == C.BUY:
            oflags.append('viqc')
            balance_label = quote
            precision_label = 'cost_decimals'
        elif side.upper() != C.SELL:
            raise Exception('Need to specify BUY or SELL side for order')

        balance = float(self.get_balance()[balance_label])
        amount = spend_ratio * balance
        precision = pair_info[precision_label]
        volume = "{:0.0{}f}".format(amount, precision)

        data = {
            "nonce": self.gen_nonce(),
            'ordertype': 'market',
            'type': side.lower(),
            'pair': pair,
            'oflags': ','.join(oflags),
            'volume': volume,
            'validate': test or self.test
        }
        response = self.make_auth_req(url, data)
        return response

    def handle_response(self, response):
        response = response.json()
        error = response['error']
        if error:
            raise Exception(error)
        return response['result']

    def get_order(self, order_id):
        access = 'private'
        endpoint = 'QueryOrders'
        parts = [
            '',
            self.version,
            access,
            endpoint,
        ]
        url = '/'.join(parts)
        data = {
            "nonce": self.gen_nonce(),
            'txid': order_id,
            'trades': True
        }
        response = self.make_auth_req(url, data)
        order = response[order_id]
        order['order_id'] = order_id
        return order

    def get_trades(self, trade_ids):
        access = 'private'
        endpoint = 'QueryTrades'
        parts = [
            '',
            self.version,
            access,
            endpoint,
        ]
        url = '/'.join(parts)
        data = {
            "nonce": self.gen_nonce(),
            'txid': ','.join(trade_ids),
            'trades': True
        }
        response = self.make_auth_req(url, data)
        trades = [
            {
                **response[trade_id],
                **{'trade_id': trade_id}
            }
            for trade_id in trade_ids
        ]
        return trades

    def standardize_order(self, order, trades):
        std = {}
        std['symbol'] = order['descr']['pair']
        std['orderId'] = order['order_id']
        std['transactTime'] = int(
            (order['closetm'] + order['opentm']) / 2 * 1000)
        std['price'] = round(float(order['price']), 10)
        side = order['descr']['type'].upper()
        origQty = float(order['vol'])
        if side == C.BUY:
            # other test would be [if 'viqc' in order['oflags'].split(','):]
            origQty = round(origQty / std['price'], 10)
        std['origQty'] = origQty
        std['executedQty'] = float(order['vol_exec'])
        std['cummulativeQuoteQty'] = round(
            std['price'] * std['executedQty'], 10)
        std['status'] = order['status'].upper()
        std['type'] = order['descr']['ordertype'].upper()
        std['side'] = side

        def standardize_trade(trade):
            std_trade = {}
            std_trade['price'] = str(round(float(trade['price']), 10))
            std_trade['qty'] = trade['vol']
            std_trade['commission'] = trade['fee']
            std_trade['tradeId'] = trade['trade_id']
            return std_trade
        fills = [standardize_trade(trade) for trade in trades]
        std['fills'] = fills
        return std

    def get_test_side(self, base, quote):
        pair = f'{base}{quote}'
        pair_info = self.get_asset_pair(pair)
        balance = float(self.get_balance()[base])
        min_order = float(pair_info['ordermin'])
        side = 'buy' if balance < min_order else 'sell'
        return side


class Binance(CEX):
    def __init__(self, key=None, secret=None, testnet=False):
        super().__init__()
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
        spend_ratio = spend_ratio - C.BINANCE_FEE
        pair = self.create_pair(base, quote)
        side = side.upper()
        order_type = self.client.ORDER_TYPE_MARKET
        params = {'symbol': pair, 'type': order_type}
        symbol_info = self.client.get_symbol_info(pair)

        if side == C.SELL:
            side = self.client.SIDE_SELL
            balance_label = base
            quantity_label = 'quantity'
            filters = symbol_info['filters']
            for filter in filters:
                if filter['filterType'] == 'LOT_SIZE':
                    step_size = float(filter['stepSize'])
        elif side == C.BUY:
            side = self.client.SIDE_BUY
            balance_label = quote
            quantity_label = 'quoteOrderQty'
            precision = int(symbol_info['quoteAssetPrecision'])
        else:
            raise Exception('Need to specify BUY or SELL side for order')

        balance = float(self.client.get_asset_balance(balance_label)['free'])
        amount = spend_ratio * balance

        if side == C.BUY:
            quantity = "{:0.0{}f}".format(amount, precision)
        else:
            quantity = round_step_size(amount, step_size)

        params[quantity_label] = quantity

        params['side'] = side
        fx = self.client.create_test_order if test else self.client.create_order

        order = fx(**params)
        return order

# write script that gets most recent data at 9pm est
# predicts using model
# writes that back to predict.csv
# write successful orders to binance.csv
