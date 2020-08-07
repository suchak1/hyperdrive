import os
import json
import time
from datetime import datetime
import pandas as pd
from botocore.exceptions import ClientError
import Constants as C
from Storage import Store
# consider combining fileoperations into one class


class FileReader:
    # file read operations
    def __init__(self):
        self.store = Store()

    def load_json(self, filename):
        # loads json file as dictionary data
        with open(filename, 'r') as file:
            return json.load(file)

    def load_csv(self, filename):
        # loads csv file as Dataframe
        one_day = 60 * 60 * 24
        now = datetime.fromtimestamp(time.time())
        file_exists = os.path.exists(filename)

        if file_exists:
            then = os.path.getmtime(filename)
            delta = now - then
            last_modified = delta.total_seconds()
        try:
            if not file_exists or last_modified > one_day:
                with open(filename, 'wb') as file:
                    self.store.bucket.download_fileobj(filename, file)
            df = pd.read_csv(filename).round(10)
        except pd.errors.EmptyDataError:
            print(f'{filename} is an empty csv file.')
            raise
        except FileNotFoundError:
            print(f'{filename} does not exist locally.')
            raise
        except ClientError:
            print(f'{filename} does not exist in S3.')
            os.remove(filename)
            raise
        except Exception:
            df = pd.DataFrame()
        return df

    def check_update(self, filename, df):
        # given a csv filename and dataframe
        # return whether the csv needs to be updated
        return len(df) >= len(self.load_csv(filename))

    def update_df(self, filename, new, column):
        old = self.load_csv(filename)
        if not old.empty:
            old = old[~old[column].isin(new[column])]
            new = old.append(new, ignore_index=True)
        return new


class FileWriter:
    # file write operations
    def __init__(self):
        self.store = Store()

    def save_json(self, filename, data):
        # saves data as json file with provided filename
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def save_csv(self, filename, data):
        # saves df as csv file with provided filename
        with open(filename, 'w') as f:
            data.to_csv(f, index=False)
        self.store.upload_file(filename)

    def update_csv(self, filename, df):
        # update csv if needed
        if FileReader().check_update(filename, df):
            self.save_csv(filename, df)

# add function that takes in a Constants directory, old to new column mapping
# and renames the cols using df.rename(columns=mapping) for all csvs in the dir


class PathFinder:
    def get_symbols_path(self):
        # return the path for the symbols reference csv
        return os.path.join(
            C.DATA_DIR,
            'symbols.csv'
        )

    def get_dividends_path(self, symbol):
        # given a symbol
        # return the path to its csv
        return os.path.join(
            C.DATA_DIR,
            C.DIV_DIR,
            f'{symbol.upper()}.csv'
        )

    def get_splits_path(self, symbol):
        # given a symbol
        # return the path to its stock splits
        return os.path.join(
            C.DATA_DIR,
            C.SPLT_DIR,
            f'{symbol.upper()}.csv'
        )

    def get_all_paths(self, path, truncate=False):
        # given a path, get all sub paths
        paths = []
        for root, _, files in os.walk(path):
            for file in files:
                curr_path = os.path.join(root, file)[
                    len(path) + 1 if truncate else 0:]
                to_skip = ['__pycache__/', '.pytest',
                           '.git/', '.ipynb', '.env']
                keep = [skip not in curr_path for skip in to_skip]
                # remove caches but keep workflows
                if all(keep) or '.github' in curr_path:
                    # print(curr_path)
                    paths.append(curr_path)
        return paths


# FileReader().get_all_paths('.')
