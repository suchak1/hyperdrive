import sys
sys.path.append('src')
from Storage import Store  # noqa autopep8

store = Store()

bucket = store.get_bucket()

symbols = ['IAC', 'OTIS', 'VTRS']

def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]

for symbol in symbols:
	keys = [obj.key for obj in bucket.objects.filter(Prefix=f'data/intraday/polygon/{symbol}\\')]
	keys = chunks(keys, 500)
	for key in keys:
		store.delete_objects(key)