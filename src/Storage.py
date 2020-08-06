import os
import boto3
from dotenv import load_dotenv
from multiprocessing import Pool
from FileOps import PathFinder


class Uploader:
    def __init__(self):
        load_dotenv()
        self.bucket = os.environ.get('S3_BUCKET')
        self.finder = PathFinder()

    def upload_file(self, path):
        with open(path, 'rb') as data:
            s3 = boto3.resource('s3')
            s3.Bucket(self.bucket).put_object(Key=path, Body=data)

    def upload_dir(self, path, truncate=False):
        paths = self.finder.get_all_paths(path, truncate=truncate)
        with Pool() as p:
            p.map(self.upload_file, paths)


# class Downloader:
#     pass
