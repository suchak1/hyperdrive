import sys
import json
import pytest
import numpy as np
sys.path.append('hyperdrive')
from Transformer import NumpyEncoder  # noqa autopep8


encoder = NumpyEncoder()


class TestNumpyEncoder:
    def test_default(self):
        # list
        arr = np.array([True, False])
        with pytest.raises(TypeError):
            json.dumps(arr)
        assert json.dumps(NumpyEncoder().default(arr)) == '[true, false]'

        # bool
        val = np.True_
        with pytest.raises(TypeError):
            json.dumps(val)
        assert json.dumps(NumpyEncoder().default(val)) == 'true'

        # int
        val = np.int64(1)
        with pytest.raises(TypeError):
            json.dumps(val)
        assert json.dumps(NumpyEncoder().default(val)) == '1'

        # # float
        # val = np.float64(0.5)
        # with pytest.raises(TypeError):
        #     json.dumps(val)
        # assert json.dumps(NumpyEncoder().default(val)) == '0.5'

        # # complex
        # val = np.complex64(1 + 2j)
        # with pytest.raises(TypeError):
        #     json.dumps(arr)
        # assert json.dumps(NumpyEncoder().default(val)
        #                   ) == '{"real": 1, "imag": 2}'

        # none

        # other
        arr = []
        with pytest.raises(TypeError):
            json.dumps(NumpyEncoder().default(arr))
        assert json.dumps(arr) == '[]'
