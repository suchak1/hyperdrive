import os
import sys
sys.path.append('src')
from Algotrader import Scarlett  # noqa autopep8
import Constants as C  # noqa autopep8


sl = Scarlett()
if not C.CI:
    sl.broker.writer.store.bucket_name = os.environ['S3_DEV_BUCKET']
    sl.broker.reader.store.bucket_name = os.environ['S3_DEV_BUCKET']


class TestScarlett:
    def test_init(self):
        assert type(sl).__name__ == 'Scarlett'
        assert hasattr(sl, 'broker')
