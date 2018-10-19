from config import TS
from tester import test
from reader import load_settings_from_report
from assets import Asset
from datetime import datetime

RANDOM = True

if RANDOM:
    params = TS.get_random_params()
else:
    params = load_settings_from_report('_evo_mod.txt')

chart = Asset()
chart.load_mt4_history('MTDATA', 'ADBE', 1440)
chart.range_from_last(550)

t1 = datetime.now()
res = test(chart, params, verbose=True)

print (res['PROFIT'])
t2 = datetime.now()
print(t2-t1)
