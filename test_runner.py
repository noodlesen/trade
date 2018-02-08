
from evo import get_random_params
from tester2 import test
from reader import read_mt_csv, load_settings_from_report
from holder import Asset

RANDOM = True

if RANDOM:
    params = get_random_params()
else:
    params = load_settings_from_report('_jpy_60.txt')

data = read_mt_csv('USDJPY', timeframe=60, cut=2000)

res = test('USDJPY', data, params, verbose=True)

print (res['PROFIT'])