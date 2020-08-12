import os
import shutil
import sys
import pytest
from botocore.exceptions import ClientError
from dotenv import load_dotenv
sys.path.append('src')
from Storage import Store  # noqa autopep8
import Constants as C  # noqa autopep8

load_dotenv()
store = Store()

if not os.environ.get('CI'):
    store.bucket_name = os.environ['S3_DEV_BUCKET']

symbols_path = store.finder.get_symbols_path()
test_file1 = f'{C.DEV_DIR}/x'
test_file2 = f'{C.DEV_DIR}/y'


class TestStore:
    def test_init(self):
        assert type(store).__name__ == 'Store'
        assert hasattr(store, 's3')
        assert hasattr(store, 'bucket_name')
        assert hasattr(store, 'bucket')
        assert hasattr(store, 'finder')

    def test_upload_file(self):
        store.finder.make_path(test_file1)
        with open(test_file1, 'w') as file:
            file.write('a')
        store.upload_file(test_file1)
        assert store.key_exists(test_file1)

    def test_upload_dir(self):
        with open(test_file2, 'w') as file:
            file.write('b')
        store.upload_dir(C.DEV_DIR)
        assert store.key_exists(test_file2)

    def test_delete_objects(self):
        shutil.rmtree(C.DEV_DIR)
        store.delete_objects([test_file1, test_file2])
        assert not store.key_exists(test_file2)

    def test_get_all_keys(self):
        keys = set(store.get_all_keys())

        assert symbols_path in keys
        assert 'README.md' in keys

    def test_key_exists(self):
        assert store.key_exists(symbols_path)
        assert not store.key_exists(test_file1)

    def test_download_file(self):
        assert not os.path.exists(test_file1)
        with pytest.raises(ClientError):
            store.download_file(test_file1)
        assert not os.path.exists(test_file1)

        if os.path.exists(symbols_path):
            os.remove(symbols_path)
        assert not os.path.exists(symbols_path)
        store.download_file(symbols_path)
        assert os.path.exists(symbols_path)
