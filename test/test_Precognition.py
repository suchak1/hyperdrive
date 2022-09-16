import re
import sys
sys.path.append('hyperdrive')
from Precognition import Oracle  # noqa autopep8

oracle = Oracle()


def replace_attr(obj, find_key, replace_val):
    try:
        getattr(obj, find_key)
        setattr(obj, find_key, replace_val)
        return obj
    except AttributeError:
        attrs = [attr for attr in dir(obj) if not (
            attr.startswith('__') and attr.endswith('__'))]
        for key in attrs:
            setattr(obj, key, replace_attr(
                getattr(obj, key), find_key, replace_val))
        return obj


class TestOracle:
    def test_init(self):
        # assert type(oracle).__name__ == 'Oracle'
        # assert hasattr(oracle, 'writer')
        # assert hasattr(oracle, 'reader')
        # assert hasattr(oracle, 'calc')
        ora = replace_attr(oracle, 'bucket_name', '123')
        print(ora.reader.store.bucket_name)
        print(ora.writer.store.bucket_name)

    def test_filename(self):
        pass

    def test_load_model_pickle(self):
        pass

    def test_save_model_pickle(self):
        pass

    def test_predict(self):
        pass

    def test_visualizes(self):
        pass
