import os
import sys
sys.path.append('src')
from Algotrader import HyperDrive  # noqa autopep8
import Constants as C  # noqa autopep8


drive = HyperDrive()
if not C.CI:
    drive.broker.writer.store.bucket_name = os.environ['S3_DEV_BUCKET']
    drive.broker.reader.store.bucket_name = os.environ['S3_DEV_BUCKET']


class TestHyperDrive:
    def test_init(self):
        assert type(drive).__name__ == 'HyperDrive'
        assert hasattr(drive, 'broker')
