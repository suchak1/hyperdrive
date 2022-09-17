import os
import sys
sys.path.append('hyperdrive')
from Precognition import Oracle  # noqa autopep8
from Utils import SwissArmyKnife  # noqa autopep8


knife = SwissArmyKnife()
oracle = Oracle()
oracle = knife.use_dev(oracle)
name = 'dir/file'
actual = oracle.get_filename(name)


class TestOracle:
    def test_init(self):
        assert type(oracle).__name__ == 'Oracle'
        assert hasattr(oracle, 'writer')
        assert hasattr(oracle, 'reader')
        assert hasattr(oracle, 'calc')

    def test_filename(self):
        expected = f'models/latest/{name}.pkl'
        assert actual == expected

    def test_save_model_pickle(self):
        assert oracle.save_model_pickle(name, 'test')
        assert oracle.reader.check_file_exists(actual)

    def test_load_model_pickle(self):
        pass

    def test_predict(self):
        pass

    def test_visualize(self):
        pass
