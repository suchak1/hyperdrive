import sys
sys.path.append('hyperdrive')
from DataSource import LaborStats  # noqa

bls = LaborStats()
bls.save_unemployment_rate(timeframe='2y')
