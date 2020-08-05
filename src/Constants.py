import os

# File Paths
DATA_DIR = 'data'
DIV_DIR = 'dividends'
SPLT_DIR = 'splits'
FULL_DIV_DIR = os.path.join(DATA_DIR, DIV_DIR)

# Column Names
# Symbols / Generic
SYMBOL = 'Symbol'
NAME = 'Name'
DATE = 'Date'

# Dividends
DIV = 'Div'
EX = 'Ex'    # Ex Dividend Date
DEC = 'Dec'  # Declaration Date
PAY = 'Pay'  # Payment Date


class PathFinder:
    def get_symbols_path(self):
        # return the path for the symbols reference csv
        return os.path.join(
            DATA_DIR,
            'symbols.csv'
        )

    def get_dividends_path(self, symbol):
        # given a symbol
        # return the path to its csv
        return os.path.join(
            DATA_DIR,
            DIV_DIR,
            f'{symbol.upper()}.csv'
        )

    def get_splits_path(self, symbol):
        # given a symbol
        # return the path to its stock splits
        return os.path.join(
            DATA_DIR,
            SPLT_DIR,
            f'{symbol.upper()}.csv'
        )
