import os
from pathlib import Path
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()


def get_env_bool(var_name):
    return bool(os.environ.get(var_name)
                and os.environ[var_name].lower() == 'true')


# Environment
DEV = get_env_bool('DEV')
CI = get_env_bool('CI')
TEST = get_env_bool('TEST')

# File Paths
# data
DATA_DIR = 'data'
DEV_DIR = 'dev'
DIV_DIR = 'dividends'
SPLT_DIR = 'splits'
OHLC_DIR = 'ohlc'
SENT_DIR = 'sentiment'
INTRA_DIR = 'intraday'
# providers
IEX_DIR = 'iexcloud'
POLY_DIR = 'polygon'
TWIT_DIR = 'stocktwits'

folders = {
    'iexcloud': IEX_DIR,
    'polygon': POLY_DIR,
    'stocktwits': TWIT_DIR
}
# PLYGN

# Column Names
# Symbols / Generic
SYMBOL = 'Symbol'
NAME = 'Name'

# Dividends
DIV = 'Div'
EX = 'Ex'    # Ex Dividend Date
DEC = 'Dec'  # Declaration Date
PAY = 'Pay'  # Payment Date

# Splits
RATIO = 'Ratio'

# OHLCV
# DATE = 'Date'
TIME = 'Time'
OPEN = 'Open'
HIGH = 'High'
LOW = 'Low'
CLOSE = 'Close'
VOL = 'Vol'
AVG = 'Avg'
TRADES = 'Trades'

# Time
TZ = timezone('US/Eastern')
DATE_FMT = '%Y-%m-%d'
TIME_FMT = '%H:%M'

# Sentiment
POS = 'Pos'
NEG = 'Neg'
DELTA = 'Delta'
TWIT_RATE = 175

# Misc
POLY_CRYPTO_SYMBOLS = [
    'X%3ABTCUSD', 'X%3AETHUSD',
    'X%3ALTCUSD', 'X%3AXMRUSD', 'X%3AIOTUSD'
]

SENTIMENT_SYMBOLS_IGNORE = {
    'SPYD', 'VWDRY', 'BPMP',
    'FOX', 'YYY', 'SDIV',
    'DIV', 'SHECY', 'PALL',
    'DWDP', 'TFCF', 'SPAR',
    'TMUSR', 'OXY+', 'BNTX^'}

DEFAULT_RETRIES = 3
DEFAULT_DELAY = 2


class PathFinder:
    def make_path(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    def get_symbols_path(self):
        # return the path for the symbols reference csv
        return os.path.join(
            DATA_DIR,
            'symbols.csv'
        )

    def get_dividends_path(self, symbol, provider='iexcloud'):
        # given a symbol
        # return the path to its csv
        return os.path.join(
            DATA_DIR,
            DIV_DIR,
            folders[provider],
            f'{symbol.upper()}.csv'
        )

    def get_splits_path(self, symbol, provider='iexcloud'):
        # given a symbol
        # return the path to its stock splits
        return os.path.join(
            DATA_DIR,
            SPLT_DIR,
            folders[provider],
            f'{symbol.upper()}.csv'
        )

    def get_ohlc_path(self, symbol, provider='iexcloud'):
        # given a symbol
        # return the path to its ohlc data
        return os.path.join(
            DATA_DIR,
            OHLC_DIR,
            folders[provider],
            f'{symbol.upper()}.csv'
        )

    def get_sentiment_path(self, symbol, provider='stocktwits'):
        # given a symbol
        # return the path to its social sentiment data
        return os.path.join(
            DATA_DIR,
            SENT_DIR,
            folders[provider],
            f'{symbol.upper()}.csv'
        )

    def get_intraday_path(self, symbol, date, provider='iexcloud'):
        # given a symbol,
        # return the path to its intraday ohlc data
        return os.path.join(
            DATA_DIR,
            INTRA_DIR,
            folders[provider],
            symbol.upper(),
            f'{date}.csv'
        )

    def get_all_paths(self, path, truncate=False):
        # given a path, get all sub paths
        paths = []
        for root, _, files in os.walk(path):
            for file in files:
                curr_path = os.path.join(root, file)[
                    len(path) + 1 if truncate else 0:]
                to_skip = ['__pycache__/', '.pytest',
                           '.git/', '.ipynb', '.env']
                keep = [skip not in curr_path for skip in to_skip]
                # remove caches but keep workflows
                if all(keep) or '.github' in curr_path:
                    # print(curr_path)
                    paths.append(curr_path)
        return paths
