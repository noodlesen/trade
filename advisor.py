from reader import load_settings_from_report
import TS_hound as TS
from assets import MultiAsset
from stocks_list import STOCKS

mas = MultiAsset()
mas.load('mqtest.txt', 1440)


params = load_settings_from_report('results/_evo_mod_32k_2y.txt')

req = 0
for s in STOCKS:

    c = mas.assets[s]
    c.set_to_last()
    cc = c.get()

    t = TS.open(cc, c, [], params)

    
    if t:
        print (s, t.direction, 'at',t.open_price, t.open_reason)
        req+=t.open_price

print ('MARGIN_REQUIRED:',req/20)
