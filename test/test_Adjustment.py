import sys
import pandas as pd
sys.path.append('src')
from Adjustment import SplitWorker  # noqa autopep8
import Constants as C  # noqa autopep8


worker = SplitWorker()
data = {C.TIME: ['2021-07-15', '2021-07-16',
                 '2021-07-19', '2021-07-20'],
        C.OPEN: [792.4700, 761.2200, 179.1525, 187.3000],
        C.CLOSE: [758.6500, 726.4400, 187.7975, 186.1200]}
df = pd.DataFrame(data)
date = None


class TestSplitWorker:
    def test_init(self):
        assert hasattr(worker, 'md')

    def test_get_recent_splits(self):
        dfs = worker.get_recent_splits(['NVDA', 'TSLA', 'AAPL'], '5y')
        assert len(dfs) > 0 and len(dfs) <= 3

    def test_find_split_row(self):
        date = worker.find_split_row(df, pd.to_datetime('2021-07-20'), 0.25)
        assert date == '2021-07-19'

    def test_apply_split(self):
        split_df = worker.apply_split(df, date, 0.25)
        test_data = {C.TIME: ['2021-07-15', '2021-07-16',
                              '2021-07-19', '2021-07-20'],
                     C.OPEN: [198.1200, 190.3000, 179.1525, 187.3000],
                     C.CLOSE: [189.6600, 181.6100, 187.7975, 186.1200]}
        test_df = pd.DataFrame(test_data)
        assert split_df.equals(test_df)

    # REMEMBER that apply_split needs date from find_split_row!
