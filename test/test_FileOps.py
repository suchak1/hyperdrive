import os
import sys
import pandas as pd
sys.path.append('src')
from FileOps import FileReader, FileWriter  # noqa autopep8
import Constants as C  # noqa autopep8

reader = FileReader()
writer = FileWriter()

run_id = ''
if not C.CI:
    reader.store.bucket_name = os.environ['S3_DEV_BUCKET']
    writer.store.bucket_name = os.environ['S3_DEV_BUCKET']
else:
    run_id = os.environ['RUN_ID']

symbols_path = reader.store.finder.get_symbols_path()

json_path1 = 'test/test1.json'
json_path2 = 'test/test2.json'

csv_path1 = f'test/test1_{run_id}.csv'
csv_path2 = f'test/test2_{run_id}.csv'

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

test_df = pd.DataFrame(data)
big_df = pd.DataFrame(data_)
small_df = pd.DataFrame([snippet])
empty_df = pd.DataFrame()


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
        filename = f'{C.DEV_DIR}/{run_id}_x'
        assert not reader.check_file_exists(filename)
        reader.store.finder.make_path(filename)
        with open(filename, 'w') as file:
            file.write('123')
        writer.store.upload_file(filename)
        assert reader.check_file_exists(filename)
        writer.remove_files([filename])
        assert not reader.check_file_exists(filename)

    def test_rename_file(self):
        src_path = f'{symbols_path}_{run_id}_SRC1'
        dst_path = f'{symbols_path}_{run_id}_DST1'

        assert not reader.check_file_exists(src_path)
        writer.store.copy_object(symbols_path, src_path)
        writer.store.download_file(src_path)
        assert reader.check_file_exists(src_path)

        assert not reader.check_file_exists(dst_path)
        writer.rename_file(src_path, dst_path)
        assert reader.check_file_exists(dst_path)

        writer.remove_files([dst_path])


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
        assert not reader.check_file_exists('test_check_file_exists')
        assert reader.check_file_exists(symbols_path)
