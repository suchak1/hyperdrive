import os
import sys
sys.path.append('src')
from scarlett import Scarlett  # noqa autopep8

sl = Scarlett(os.environ['EMAIL'], os.environ['PASSWORD'])
