import os
import sys
from datetime import timedelta
import pytest
import pandas as pd
sys.path.append('src')
from FileOps import FileReader, FileWriter  # noqa autopep8
import Constants as C  # noqa autopep8

dir_path = os.path.dirname(os.path.realpath(__file__))
json_path1 = os.path.join(dir_path, 'test1.json')
json_path2 = os.path.join(dir_path, 'test2.json')

empty = {}
data = [
    {
        'symbol': 'AMZN',
        'open': 2400.85,
        'volume': 402265,
        'date': '2020-12-25'
    },
    {
        'symbol': 'AAPL',
        'open': 300.90,
        'volume': 502265,
        'date': '2015-01-15'
    }
]
snippet = {
    'symbol': 'NVDA',
    'open': 445.00,
    'volume': 102265,
    'date': '2015-01-15'
}
data_ = data[:]
data_.append(snippet)

csv_path1 = os.path.join(dir_path, 'test1.csv')
csv_path2 = os.path.join(dir_path, 'test2.csv')
test_df = pd.DataFrame(data)
big_df = pd.DataFrame(data_)
small_df = pd.DataFrame([snippet])
empty_df = pd.DataFrame()

reader = FileReader()
writer = FileWriter()
symbols_path = reader.store.finder.get_symbols_path()
test_path = f'{symbols_path}_TEST'


class TestFileWriter:
    def test_init(self):
        assert type(writer).__name__ == 'FileWriter'
        assert hasattr(reader, 'store')

    def test_save_json(self):
        # save empty json object
        writer.save_json(json_path1, {})
        assert os.path.exists(json_path1)

        # save list of 2 json objects
        writer.save_json(json_path2, data)
        assert os.path.exists(json_path2)

    def test_save_csv(self):
        # save empty table
        assert not writer.save_csv(csv_path1, empty_df)
        assert not reader.check_file_exists(csv_path1)

        # save table with 2 rows
        assert writer.save_csv(csv_path2, test_df)
        assert reader.check_file_exists(csv_path2)

    def test_update_csv(self):
        writer.update_csv(csv_path2, test_df)
        assert reader.load_csv(csv_path2).equals(test_df)

        writer.update_csv(csv_path2, small_df)
        assert reader.load_csv(csv_path2).equals(test_df)
        assert not reader.load_csv(csv_path2).equals(small_df)

        writer.update_csv(csv_path2, big_df)
        assert reader.load_csv(csv_path2).equals(big_df)
        assert not reader.load_csv(csv_path2).equals(test_df)

        writer.save_csv(csv_path2, test_df)

    def test_remove_files(self):
        filename = f'{C.DEV_DIR}/x'
        assert not reader.check_file_exists(filename)
        reader.store.finder.make_path(filename)
        with open(filename, 'w') as file:
            file.write('a')
        writer.store.upload_file(filename)
        assert reader.check_file_exists(filename)
        writer.remove_files([filename])
        assert not reader.check_file_exists(filename)

    def test_rename_file(self):
        assert not reader.check_file_exists(test_path)
        if not os.path.exists(symbols_path):
            writer.store.download_file(symbols_path)
        writer.rename_file(symbols_path, test_path)
        assert reader.check_file_exists(test_path)
        writer.rename_file(test_path, symbols_path)


class TestFileReader:
    def test_init(self):
        assert type(reader).__name__ == 'FileReader'
        assert hasattr(reader, 'store')

    def test_load_json(self):
        # empty case from above
        assert reader.load_json(json_path1) == empty
        # mock data case from above
        assert reader.load_json(json_path2) == data

        os.remove(json_path1)
        os.remove(json_path2)

    def test_load_csv(self):
        # empty case from above
        assert reader.load_csv(csv_path1).equals(empty_df)
        # mock data case from above
        assert reader.load_csv(csv_path2).equals(test_df)

    def test_check_update(self):
        assert reader.check_update(csv_path2, test_df)
        assert not reader.check_update(csv_path2, small_df)
        assert reader.check_update(csv_path2, big_df)

    def test_update_df(self):
        assert reader.update_df(csv_path2, test_df, 'date').equals(test_df)
        assert reader.update_df(csv_path2, big_df, 'date').equals(big_df)

        writer.remove_files([csv_path2])

    def test_check_file_exists(self):
        assert not reader.check_file_exists('a')
        assert reader.check_file_exists(symbols_path)

    def test_convert_delta(self):
        assert reader.convert_delta('1d') == timedelta(days=1)
        assert reader.convert_delta('3d') == timedelta(days=3)

        assert reader.convert_delta('1w') == timedelta(days=7)
        assert reader.convert_delta('3w') == timedelta(days=21)

        assert reader.convert_delta('1m') == timedelta(days=30)
        assert reader.convert_delta('3m') == timedelta(days=90)

        assert reader.convert_delta('1y') == timedelta(days=365)
        assert reader.convert_delta('3y') == timedelta(days=1095)

        with pytest.raises(ValueError):
            reader.convert_delta('0')
