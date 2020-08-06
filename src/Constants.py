import os
from dotenv import load_dotenv

load_dotenv()
# Environment
DEV = bool(os.environ.get('DEV'))

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
