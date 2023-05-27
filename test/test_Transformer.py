import sys
import json
import pytest
import numpy as np
sys.path.append('hyperdrive')
from Transformer import NumpyEncoder  # noqa autopep8


encoder = NumpyEncoder()


class TestNumpyEncoder:
    def test_default(self):
        arr = np.array([True, False])
        with pytest.raises(TypeError):
            json.dumps(arr)
        assert json.dumps(NumpyEncoder().default(arr)) == '[true, false]'
