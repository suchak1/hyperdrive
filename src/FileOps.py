import os
import json
import pandas as pd

# consider combining fileoperations into one class


class FileReader:
    # file read operations
    def load_json(self, filename):
        # loads json file as dictionary data
        with open(filename, 'r') as file:
            return json.load(file)

    def load_csv(self, filename):
        # loads csv file as Dataframe
        try:
            df = pd.read_csv(filename)
        except pd.errors.EmptyDataError:
            # empty csv
            print(f'{filename} is an empty csv file.')
            df = pd.DataFrame()
        return df

    def check_update(self, filename, df):
        # given a csv filename and dataframe
        # return whether the csv needs to be updated
        return (len(df) >= len(self.load_csv(filename))
                if os.path.exists(filename) else len(df) > 0)

    def update_df(self, filename, new, column, mapper=None):
        if os.path.exists(filename):
            old = self.load_csv(filename)
            # if mapper:
            #     for col, fx in mapper.items():
            #         old[col] = fx(old[col])
            #         new[col] = fx(old[col])
            old = old[~old[column].isin(new[column])]
            new = old.append(new, ignore_index=True)
        return new


class FileWriter:
    # file write operations
    def save_json(self, filename, data):
        # saves data as json file with provided filename
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def save_csv(self, filename, data):
        # saves df as csv file with provided filename
        with open(filename, 'w') as f:
            data.to_csv(f, index=False)

    def update_csv(self, filename, df):
        # update csv if needed
        if FileReader().check_update(filename, df):
            self.save_csv(filename, df)

# add function that takes in a Constants directory, old to new column mapping
# and renames the cols using df.rename(columns=mapping) for all csvs in the dir
