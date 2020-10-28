import os
import sys
sys.path.append('src')
from DataSource import StockTwits  # noqa autopep8
from Constants import PathFinder  # noqa autopep8
import Constants as C  # noqa autopep8


twit = StockTwits()
symbols = twit.get_symbols()
crypto_symbols = ['BTC-X', 'ETH-X', 'LTC-X', 'XMR-X', 'IOT-X']
if C.TEST:
    symbols = crypto_symbols
    twit.token = ''
else:
    symbols.extend(crypto_symbols)
BATCH = int(os.environ.get('BATCH')) if os.environ.get('BATCH') else 1
# better solution is to dynamically choose 175 most outdated symbols

# First batch
for symbol in symbols[C.TWIT_RATE*(BATCH-1):C.TWIT_RATE*BATCH]:
    if symbol in C.SENTIMENT_SYMBOLS_IGNORE:
        continue
    try:
        twit.save_social_sentiment(symbol=symbol, timeframe='1d',
                                   retries=1 if C.TEST else 2)
    except Exception as e:
        print(f'Stocktwits sentiment update failed for {symbol}.')
        print(e)
    finally:
        filename = PathFinder().get_sentiment_path(
            symbol=symbol, provider=twit.provider)
        if C.CI and os.path.exists(filename):
            os.remove(filename)
