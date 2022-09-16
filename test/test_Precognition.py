import re
import sys
sys.path.append('hyperdrive')
from Precognition import Oracle  # noqa autopep8

oracle = Oracle()


class TestOracle:
    def test_init(self):
        assert type(oracle).__name__ == 'Oracle'
        assert hasattr(oracle, 'writer')
        assert hasattr(oracle, 'reader')
        assert hasattr(oracle, 'calc')

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
