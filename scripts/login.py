import os
import sys
from dotenv import load_dotenv
sys.path.append('src')
from scarlett import Broker  # noqa autopep8

load_dotenv()
Broker(os.environ['EMAIL'], os.environ['PASSWORD'])
