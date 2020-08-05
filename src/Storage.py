import boto3
from dotenv import load_dotenv
from multiprocessing import Pool
from FileOps import FileReader


class Uploader:
    def __init__(self):
        load_dotenv()
        # self.s3 = boto3.resource('s3')
        self.reader = FileReader()

    def upload_file(self, path):
        with open(path, 'rb') as data:
            s3 = boto3.resource('s3')
            s3.Bucket('suchak1.scarlett').put_object(Key=path, Body=data)

    def upload_dir(self, path):
        paths = self.reader.get_all_paths(path)
        with Pool() as p:
            p.map(self.upload_file, paths)


class Downloader:
    pass
