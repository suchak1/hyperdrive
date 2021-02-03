import sys
sys.path.append('src')
from Storage import Store  # noqa autopep8

store = Store()

bucket = store.get_bucket()


def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]

keys = [obj.key for obj in bucket.objects.filter(Prefix='data\\')]
keys = chunks(keys, 500)
for key in keys:
	store.delete_objects(key)