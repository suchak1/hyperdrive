import os
import sys
sys.path.append('src')
from DataSource import StockTwits  # noqa autopep8
import Constants as C  # noqa autopep8

twit = StockTwits()
symbols = twit.get_symbols()
BATCH = int(os.environ.get('BATCH')) if os.environ.get('BATCH') else 1
# better solution is to dynamically choose 175 most outdated symbols

# First batch
for symbol in symbols[C.TWIT_RATE*(BATCH-1):C.TWIT_RATE*BATCH]:
    if symbol == 'HD':
        try:
            twit.save_social_sentiment(symbol=symbol, timeframe='1d')
        except Exception as e:
            print(f'Stocktwits sentiment update failed for {symbol}.')
            print(e)
