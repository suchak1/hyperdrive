import os
import sys
sys.path.append('hyperdrive')
from DataSource import Glassnode  # noqa autopep8
import Constants as C  # noqa autopep8

counter = 0
glass = Glassnode()

try:
    filename = glass.save_s2f_ratio(
        timeframe='max', retries=1 if C.TEST else 2)
    counter += 1
    if C.CI and os.path.exists(filename):
        os.remove(filename)
except Exception as e:
    print('Glassnode S2F update failed.')
    print(e)

try:
    filename = glass.save_diff_ribbon(
        timeframe='max', retries=1 if C.TEST else 2)
    counter += 1
    if C.CI and os.path.exists(filename):
        os.remove(filename)
except Exception as e:
    print('Glassnode Diff Ribbon update failed.')
    print(e)

try:
    filename = glass.save_sopr(timeframe='max', retries=1 if C.TEST else 2)
    counter += 1
    if C.CI and os.path.exists(filename):
        os.remove(filename)
except Exception as e:
    print('Glassnode SOPR update failed.')
    print(e)

if counter < 3:
    exit(1)
