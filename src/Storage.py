import os
import boto3
from dotenv import load_dotenv
from multiprocessing import Pool
from FileOps import PathFinder
import Constants as C


class Store:
    def __init__(self):
        load_dotenv()
        self.s3 = boto3.resource('s3')
        self.bucket_name = os.environ.get(
            'S3_BUCKET') if not C.DEV else os.environ.get('S3_DEV_BUCKET')
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.finder = PathFinder()

    def upload_file(self, path):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket_name)
        bucket.upload_file(path, path)

    def upload_dir(self, path, truncate=False):
        paths = self.finder.get_all_paths(path, truncate=truncate)
        with Pool() as p:
            p.map(self.upload_file, paths)

    def delete_objects(self, keys):
        objects = [{'Key': key} for key in keys]
        self.bucket.delete_objects(Delete={'Objects': objects})

    def get_all_keys(self):
        keys = [obj.key for obj in self.bucket.objects.filter()]
        return keys


# class Downloader:
#     pass
