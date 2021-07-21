import os
import sys
sys.path.append('src')
from DataSource import Glassnode  # noqa autopep8
from Constants import PathFinder  # noqa autopep8
import Constants as C  # noqa autopep8


glass = Glassnode()

try:
    glass.save_s2f(timeframe='max', retries=1 if C.TEST else 2)
except Exception as e:
    print('Glassnode S2F update failed.')
    print(e)
finally:
    filename = PathFinder().get_s2f_path()
    if C.CI and os.path.exists(filename):
        os.remove(filename)
