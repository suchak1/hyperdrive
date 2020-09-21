import sys
sys.path.append('src')
from DataSource import StockTwits  # noqa autopep8

twit = StockTwits()
# symbols = twit.get_symbols()
symbols = ['TSLA']


for symbol in symbols:
    try:
        twit.save_social_sentiment(symbol=symbol)
    except Exception as e:
        print(f'Stocktwits sentiment update failed for {symbol}.')
        print(e)
