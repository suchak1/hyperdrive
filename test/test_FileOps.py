import os
import sys
import pandas as pd
sys.path.append('src')
from FileOps import FileReader, FileWriter  # noqa autopep8

dir_path = os.path.dirname(os.path.realpath(__file__))
json_path1 = os.path.join(dir_path, 'test1.json')
json_path2 = os.path.join(dir_path, 'test2.json')

empty = {}
data = [
    {
        'symbol': 'AMZN',
        'open': 2400.85,
        'volume': 402265
    },
    {
        'symbol': 'AAPL',
        'open': 300.90,
        'volume': 502265

    }
]

csv_path1 = os.path.join(dir_path, 'test1.csv')
csv_path2 = os.path.join(dir_path, 'test2.csv')
test_df = pd.DataFrame(data)
empty_df = pd.DataFrame()

reader = FileReader()
writer = FileWriter()


class TestFileWriter:
    def test_init(self):
        assert type(writer).__name__ == 'FileWriter'

    def test_save_json(self):
        # save empty json object
        writer.save_json(json_path1, {})
        assert os.path.exists(json_path1)

        # save list of 2 json objects
        writer.save_json(json_path2, data)
        assert os.path.exists(json_path2)

    def test_save_csv(self):
        # save empty table
        writer.save_csv(csv_path1, empty_df)
        assert os.path.exists(csv_path1)

        # save table with 2 rows
        writer.save_csv(csv_path2, test_df)
        assert os.path.exists(csv_path2)


class TestFileReader:
    def test_init(self):
        assert type(reader).__name__ == 'FileReader'

    def test_load_json(self):
        # empty case from above
        assert reader.load_json(json_path1) == empty
        # mock data case from above
        assert reader.load_json(json_path2) == data

    def test_load_csv(self):
        # empty case from above
        assert reader.load_csv(csv_path1).equals(empty_df)
        # mock data case from above
        assert reader.load_csv(csv_path2).equals(test_df)
