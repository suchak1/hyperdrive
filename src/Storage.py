import boto3
from FileOps import FileReader


class Uploader:
    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.reader = FileReader()


class Downloader:
    pass
