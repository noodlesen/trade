
from evo import get_random_params
from tester2 import test
from reader import read_mt_csv, load_settings_from_report
from holder import Asset
from datetime import datetime

RANDOM = True

if RANDOM:
    params = get_random_params()
else:
    params = load_settings_from_report('_jpy_60.txt')

#data = read_mt_csv('USDJPY', timeframe=60, cut=2000)

chart = Asset()
chart.load_mt4_history('MTDATA','ADBE', 1440)
chart.range_from_last(500)

#chart.require(['high_-250~0_max'])
#print(chart.data)

#chart.last(5)
t1 = datetime.now()
res = test(chart, params, verbose=True)

print (res['PROFIT'])
t2 = datetime.now()
print(t2-t1)