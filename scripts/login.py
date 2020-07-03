import os
import sys
from dotenv import load_dotenv
sys.path.append('src')
from scarlett import Scarlett  # noqa autopep8

load_dotenv()
sl = Scarlett(os.environ['EMAIL'], os.environ['PASSWORD'])
