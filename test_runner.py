
from evo import get_random_params
from tester import test
from reader import read_mt_csv



data = read_mt_csv('USDCHF', timeframe=1440, cut=2000)

res = test('USDCHF', data, get_random_params(), verbose=True)

print (res['PROFIT'])