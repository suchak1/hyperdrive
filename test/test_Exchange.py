import sys
sys.path.append('hyperdrive')
from Exchange import Binance  # noqa autopep8
bn = Binance(testnet=True)


class TestBinance:
    def test_init(self):
        assert type(bn).__name__ == 'Binance'
        assert hasattr(bn, 'key')
        assert hasattr(bn, 'secret')
        assert hasattr(bn, 'client')

    def test_order(self):
        base = 'BTC'
        quote = 'USDT'
        bn.order(base, quote, 'buy', 0.01, test=True)

    # selling btc response
    # {'symbol': 'BTCUSD', 'orderId': 664894061, 'orderListId': -1,
    # 'clientOrderId': 'EACZgyd3kO4r28V2Che5x9', 'transactTime': 1634612257816,
    # 'price': '0.0000', 'origQty': '0.00080000', 'executedQty': '0.00080000',
    # 'cummulativeQuoteQty': '49.4641', 'status': 'FILLED', 'timeInForce':
    # 'GTC', 'type': 'MARKET', 'side': 'SELL', 'fills': [{'price':
    # '61830.1400', 'qty': '0.00080000', 'commission': '0.0500',
    # 'commissionAsset': 'USD', 'tradeId': 24328534}]}

    # buying btc response
    # {'symbol': 'BTCUSD', 'orderId': 664895034, 'orderListId': -1,
    # 'clientOrderId': 'S3ALGacJPWtYZ8IKLnTAXE', 'transactTime': 1634612303994,
    # 'price': '0.0000', 'origQty': '0.00079900', 'executedQty': '0.00079900',
    # 'cummulativeQuoteQty': '49.3823', 'status': 'FILLED', 'timeInForce':
    # 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{'price':
    # '61805.2400', 'qty': '0.00079900', 'commission': '0.00000080',
    # 'commissionAsset': 'BTC', 'tradeId': 24328549}]}

    # symbol_info response
    # {'baseAsset': 'BTC',
    #  'baseAssetPrecision': 8,
    #  'baseCommissionPrecision': 8,
    #  'filters': [{'filterType': 'PRICE_FILTER',
    #               'maxPrice': '100000.0000',
    #               'minPrice': '0.0100',
    #               'tickSize': '0.0100'},
    #              {'avgPriceMins': 5,
    #               'filterType': 'PERCENT_PRICE',
    #               'multiplierDown': '0.2',
    #               'multiplierUp': '5'},
    #              {'filterType': 'LOT_SIZE',
    #               'maxQty': '9000.00000000',
    #               'minQty': '0.00000100',
    #               'stepSize': '0.00000100'},
    #              {'applyToMarket': True,
    #               'avgPriceMins': 5,
    #               'filterType': 'MIN_NOTIONAL',
    #               'minNotional': '10.0000'},
    #              {'filterType': 'ICEBERG_PARTS', 'limit': 10},
    #              {'filterType': 'MARKET_LOT_SIZE',
    #               'maxQty': '3200.00000000',
    #               'minQty': '0.00000000',
    #               'stepSize': '0.00000000'},
    #              {'filterType': 'MAX_NUM_ORDERS', 'maxNumOrders': 200},
    #              {'filterType': 'MAX_NUM_ALGO_ORDERS', 'maxNumAlgoOrders': 5}
    # ],
    #  'icebergAllowed': True,
    #  'isMarginTradingAllowed': False,
    #  'isSpotTradingAllowed': True,
    #  'ocoAllowed': True,
    #  'orderTypes': ['LIMIT',
    #                 'LIMIT_MAKER',
    #                 'MARKET',
    #                 'STOP_LOSS_LIMIT',
    #                 'TAKE_PROFIT_LIMIT'],
    #  'permissions': ['SPOT'],
    #  'quoteAsset': 'USD',
    #  'quoteAssetPrecision': 4,
    #  'quoteCommissionPrecision': 2,
    #  'quoteOrderQtyMarketAllowed': True,
    #  'quotePrecision': 4,
    #  'status': 'TRADING',
    #  'symbol': 'BTCUSD'}
