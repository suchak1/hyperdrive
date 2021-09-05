import os
import sys
sys.path.append('src')
from DataSource import StockTwits  # noqa autopep8
from Constants import PathFinder  # noqa autopep8
import Constants as C  # noqa autopep8


twit = StockTwits()
no_auth_twit = StockTwits()
no_auth_twit.token = ''
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

current_batch = symbols[C.TWIT_RATE*(BATCH-1):C.TWIT_RATE*BATCH]
num_failed = 0

for symbol in current_batch:
    if symbol in C.SENTIMENT_SYMBOLS_IGNORE:
        continue
    try:
        twit.save_social_sentiment(symbol=symbol, timeframe='30d',
                                   retries=1)
    except Exception as e:
        try:
            no_auth_twit.save_social_sentiment(symbol=symbol, timeframe='30d',
                                               retries=1)
        except Exception as e2:
            num_failed += 1
            print(f'Stocktwits sentiment update failed for {symbol}.')
            print(e)
            print(e2)
    finally:
        filename = PathFinder().get_sentiment_path(
            symbol=symbol, provider=twit.provider)
        if C.CI and os.path.exists(filename):
            os.remove(filename)

if num_failed / len(current_batch) > 0.5:
    raise Exception('Majority failure.')
