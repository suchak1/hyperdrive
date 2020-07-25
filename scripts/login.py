import os
import sys
sys.path.append('src')
from scarlett import Scarlett  # noqa autopep8

sl = Scarlett(os.environ['RH_USERNAME'], os.environ['RH_PASSWORD'])
