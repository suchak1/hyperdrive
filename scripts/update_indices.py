import sys
sys.path.append('hyperdrive')
from DataSource import Indices  # noqa autopep8

idc = Indices()

idc.save_ndx()
