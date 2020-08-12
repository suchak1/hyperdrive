import sys
sys.path.append('src')
from Storage import Store  # noqa autopep8
from Constants import DATA_DIR  # noqa autopep8

store = Store()
repo_keys = [key for key in store.get_all_keys()
             if key.find(f'{DATA_DIR}/')]
store.delete_objects(repo_keys)
store.upload_dir('.', truncate=True)
