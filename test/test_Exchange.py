from pprint import pprint
import sys
sys.path.append('src')
from Exchange import Binance  # noqa autopep8
bn = Binance(testnet=True)


class TestBinance:
    def test_init(self):
        assert type(bn).__name__ == 'Binance'
        assert hasattr(bn, 'key')
        assert hasattr(bn, 'secret')
        assert hasattr(bn, 'client')

    def test_order(self):
        # _to = 'BTC'
        _to = 'BNB'
        _from = 'USDT'
        symbol = f'{_to}{_from}'

        quantity, price = bn.calculate_order(_to, _from, 1)
        print('\n')
        print('quantity: ', quantity)

        # quantity, price = bn.calculate_order('BTC', 'USDT', 1.01)
        # limit order
        # order = bn.order4real(symbol, 'buy', quantity, price)
        # market order
        order = bn.order(symbol, 'sell', quantity)
        print(order)

        # prices = bn.client.get_all_tickers()
        # print(prices)

    def test_get_asset_balance(self):
        balances = {}
        for symbol in ['USDT', 'BNB', 'BTC', 'USD', 'BUSD', 'USDC']:
            balances[symbol] = bn.get_asset_balance(symbol)
        print('\n')
        pprint(balances)
