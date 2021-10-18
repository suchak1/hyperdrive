import os
import math
from binance import Client
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

    def get_asset_balance(self, asset):
        return self.client.get_asset_balance(asset=asset)

    def order(self, symbol, side, quantity, price=None, test=False):
        side = Client.SIDE_SELL if side.lower() == 'sell' else Client.SIDE_BUY
        order_type = (
            Client.ORDER_TYPE_LIMIT if price else Client.ORDER_TYPE_MARKET)
        time_in_force = self.client.TIME_IN_FORCE_GTC if price else None
        fx = self.client.create_order
        if test:
            fx = self.client.test_create_order

        order = fx(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity,
            price=price,
            timeInForce=time_in_force)
        return order

    def calculate_order(self, _to, _from, ratio=1):
        def floatPrecision(f, n):
            n = int(math.log10(1 / float(n)))
            f = math.floor(float(f) * 10 ** n) / 10 ** n
            f = "{:0.0{}f}".format(float(f), n)
            return str(int(f)) if int(n) == 0 else f
        symbol = f'{_to}{_from}'
        symbol_info = self.client.get_symbol_info(symbol)

        tick_size = float(list(filter(
            lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']
        ))[0]['tickSize'])
        step_size = float(list(filter(
            lambda f: f['filterType'] == 'LOT_SIZE', symbol_info['filters']
        ))[0]['stepSize'])
        price = float(list(filter(
            lambda x: x['symbol'] == symbol, self.client.get_all_tickers()
        ))[0]['price'])

        price = floatPrecision(price, tick_size)
        from_balance = float(
            self.client.get_asset_balance(asset=_from)['free'])
        quantity = floatPrecision(
            from_balance * ratio / float(price), step_size)
        print(f'\n{_from}: ', from_balance)
        print('ratio: ', ratio)
        return quantity, price

    # def order4real(self, symbol, side, quantity, price=None):
    #     side = Client.SIDE_SELL if side.lower() == 'sell' else Client.SIDE_BUY
    #     order_type = (
    #         Client.ORDER_TYPE_LIMIT if price else Client.ORDER_TYPE_MARKET)

    #     order = self.client.create_order(
    #         symbol=symbol,
    #         side=side,
    #         type=order_type,
    #         quantity=quantity,
    #         price=price,
    #         timeInForce=self.client.TIME_IN_FORCE_GTC)
    #     return order


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
