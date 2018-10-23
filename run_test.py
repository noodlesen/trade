from config import TS
from tester import test
from reader import load_settings_from_report
from assets import Asset
from datetime import datetime

RANDOM = False

if RANDOM:
    params = TS.get_random_ts_params()
else:
    params = load_settings_from_report('_evo.txt')

chart = Asset()
#chart.load_mt4_history('MTDATA', 'BA', 1440)
chart.load_av_history('AVHD', 'DISCA')
chart.range_from_last(500)


res = test(chart, params, verbose=True, draw=False)

for k,v in res.items():
    print(k, v)
print()
print ('%r(%d)' % (res['PROFIT'],res['TRADES']))

