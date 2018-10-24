from config import TS
from tester import test
from reader import load_settings_from_report
from assets import Asset
from datetime import datetime

RANDOM = False

if RANDOM:
    params = TS.get_random_ts_params()
else:
    params = load_settings_from_report('evo.txt')

chart = Asset()
chart.load_av_history('AVHD', 'AAPL')
chart.range_from_last(750)


res = test(chart, params, verbose=True, draw=False)

for k,v in res.items():
    print(k, v)
print()
print ('%r(%d)' % (res['PROFIT'],res['TRADES']))

