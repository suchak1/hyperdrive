import sys
sys.path.append('src')
from Adjustment import SplitWorker  # noqa autopep8
import Constants as C  # noqa autopep8

provider = 'polygon'
symbols = ['TSLA', 'AAPL', 'VWDRY', 'NEE', 'CP']
# if provider == 'polygon':
#     symbols.remove('VWDRY')
timeframe = '1y'
# timeframe = '18m'
worker = SplitWorker()
worker.process(symbols, timeframe, provider)
