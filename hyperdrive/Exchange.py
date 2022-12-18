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


class Kraken:
    def __init__(self):
        self.api_url = 'https://api.kraken.com'
        self.version = '0'
        self.key = os.environ['KRAKEN_KEY']
        self.secret = os.environ['KRAKEN_SECRET']

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
        req = requests.post(
            (self.api_url + uri_path),
            headers=headers,
            data=data
        )
        return req

    def gen_nonce(self):
        return str(int(1000*time.time()))

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
        return response.json()['result']

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
        return response.json()['result'][pair]

    def order(self, base, quote, side, spend_ratio=1, test=False):
        # uncomment this to account for fees
        # fee = self.get_asset_pair(pair)['fees'][0][1] / 100
        pair = f'{base}{quote}'
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
        balance_label = base
        oflags = ['nompp']
        if side == 'buy':
            oflags.append('viqc')
            balance_label = quote
        balance = float(self.get_balance()[balance_label])
        amount = spend_ratio * balance
        if side == 'buy':
            volume = "{:0.0{}f}".format(amount, precision)
        else:
            volume = round_step_size(amount, step_size)
        # volume = str(spend_ratio * balance)
        print(volume)
        data = {
            "nonce": self.gen_nonce(),
            'ordertype': 'market',
            'type': side.lower(),
            'pair': pair,
            'oflags': ','.join(oflags),
            'volume': volume,
            'validate': test
        }
        response = self.make_auth_req(url, data)
        return response.json()


class Binance:
    def __init__(self, key=None, secret=None, testnet=False):
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
