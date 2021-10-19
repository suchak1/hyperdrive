from pprint import pprint
import sys
sys.path.append('src')
from Exchange import Binance  # noqa autopep8
bn = Binance(testnet=False)


class TestBinance:
    def test_init(self):
        assert type(bn).__name__ == 'Binance'
        assert hasattr(bn, 'key')
        assert hasattr(bn, 'secret')
        assert hasattr(bn, 'client')

    def test_order(self):
        # _to = 'BTC'
        base = 'BTC'
        quote = 'USD'

        print('\n')

        # order = bn.order(base, quote, 'sell', 1, test=True)
        order = bn.order(base, quote, 'buy', 1)

        # order = bn.client.order_market_buy(symbol='BNBBTC', quantity=1)
        print(order)
        # orders = bn.client.get_open_orders(symbol='BNBBTC')
        # print(orders)
        # orders = bn.client.get_open_orders(symbol='BNBUSDT')
        # print(orders)

        # prices = bn.client.get_all_tickers()
        # print(prices)

    def test_get_asset_balance(self):
        balances = {}
        for symbol in ['USDT', 'BNB', 'BTC', 'USD', 'BUSD', 'USDC']:
            balances[symbol] = bn.client.get_asset_balance(symbol)
        print('\n')
        pprint(balances)

    # def test_get_asset_balance(self):
    #     balances = {}
    #     for symbol in ['USDT', 'BNB', 'BTC', 'USD', 'BUSD', 'USDC']:
    #         balances[symbol] = bn.get_asset_balance(symbol)
    #     print('\n')
    #     pprint(balances)
