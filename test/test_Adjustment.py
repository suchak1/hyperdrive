import sys
import pandas as pd
from datetime import datetime
sys.path.append('src')
from Adjustment import SplitWorker  # noqa autopep8
import Constants as C  # noqa autopep8


worker = SplitWorker()
ohlc_data = {C.TIME: ['2021-07-15', '2021-07-16',
                      '2021-07-19', '2021-07-20'],
             C.OPEN: [792.4700, 761.2200, 179.1525, 187.3000],
             C.CLOSE: [758.6500, 726.4400, 187.7975, 186.1200]}
ohlc_df = pd.DataFrame(ohlc_data)
ohlc_df[C.TIME] = pd.to_datetime(ohlc_data[C.TIME])
ohlc_date = None

intra_data = {C.TIME: ['2021-07-19 15:41', '2021-07-19 15:42',
                       '2021-07-19 15:43', '2021-07-20 09:30',
                       '2021-07-20 09:31'],
              C.OPEN: [745.907, 746.2, None, 187.3, 186.315],
              C.CLOSE: [746.33, 746.41, None, 186.15, 184.568]}
intra_df = pd.DataFrame(intra_data)
intra_df[C.TIME] = pd.to_datetime(intra_data[C.TIME])
intra_date = None


class TestSplitWorker:
    def test_init(self):
        assert hasattr(worker, 'md')

    def test_get_recent_splits(self):
        dfs = worker.get_recent_splits(['NVDA', 'TSLA', 'AAPL'], '5y')
        assert len(dfs) > 0 and len(dfs) <= 3

    def test_find_split_row(self):
        ohlc_date = worker.find_split_row(
            ohlc_df, pd.to_datetime('2021-07-20'), 0.25)
        assert ohlc_date == pd.to_datetime('2021-07-19')

        intra_date = worker.find_split_row(
            intra_df, pd.to_datetime('2021-07-20'), 0.25)
        assert intra_date == pd.to_datetime('2021-07-20 09:30')

    def test_apply_split(self):
        # print(ohlc_data[C.TIME])
        split_df = worker.apply_split(ohlc_df, ohlc_date, 0.25)
        test_data = {C.TIME: ['2021-07-15', '2021-07-16',
                              '2021-07-19', '2021-07-20'],
                     C.OPEN: [198.1200, 190.3000, 179.1525, 187.3000],
                     C.CLOSE: [189.6600, 181.6100, 187.7975, 186.1200]}
        test_df = pd.DataFrame(test_data)
        print(split_df)
        assert split_df.equals(test_df)

    # REMEMBER that apply_split needs date from find_split_row!
