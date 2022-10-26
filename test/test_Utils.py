import sys
sys.path.append('hyperdrive')
from Utils import SwissArmyKnife  # noqa autopep8
import Constants as C  # noqa autopep8


knife = SwissArmyKnife()


class TestSwissArmyKnife:
    def test_replace_attr(self):
        class Example:
            def __init__(self):
                self.var = 'old'
        ex = Example()
        assert ex.var == 'old'
        knife.replace_attr(ex, 'var', 'new')
        assert ex.var == 'new'

    def test_use_dev(self):
        if not C.CI:
            pass
