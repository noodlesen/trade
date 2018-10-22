from config import TS
from tester import test
from reader import load_settings_from_report
from assets import Asset
from datetime import datetime

RANDOM = False

if RANDOM:
    params = TS.get_random_params()
else:
    params = load_settings_from_report('grow.txt')

chart = Asset()
chart.load_mt4_history('MTDATA', 'BA', 1440)
chart.range_from_last(250)

t1 = datetime.now()
res = test(chart, params, verbose=True, draw=True)

print ('%r + %r(%d)' % (res['PROFIT'], res['OPEN_PROFIT'], res['OPEN_TRADES']))
# t2 = datetime.now()
#print(t2-t1)
