import os
import sys
sys.path.append('hyperdrive')
from DataSource import StockTwits  # noqa autopep8
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
        filename = twit.save_social_sentiment(
            symbol=symbol, timeframe='1d', retries=1)
        if C.CI and os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        try:
            filename = no_auth_twit.save_social_sentiment(
                symbol=symbol, timeframe='1d', retries=1)
            if C.CI and os.path.exists(filename):
                os.remove(filename)
        except Exception as e2:
            num_failed += 1
            print(f'Stocktwits sentiment update failed for {symbol}.')
            print(e)
            print(e2)

if num_failed / len(current_batch) > 0.5:
    raise Exception('Majority failure.')
