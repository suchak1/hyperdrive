import sys
sys.path.append('src')
from Storage import Uploader  # noqa autopep8

Uploader().upload_dir('.', truncate=True)
