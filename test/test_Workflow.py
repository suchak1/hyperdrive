import sys
from datetime import datetime
sys.path.append('src')
from Workflow import Flow  # noqa autopep8

flow = Flow()
now = datetime.utcnow()


class TestWorkFlow:
    def test_get_workflow_start_time(self):
        assert flow.get_workflow_start_time('dividends') == datetime(
            now.year, now.month, 1, 12)

    def test_is_workflow_running(self):
        pass

    def test_is_any_workflow_running(self):
        pass
