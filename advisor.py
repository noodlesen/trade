from reader import read_multi_csv, load_settings_from_report
import TS_hound as TS
from assets import MultiAsset
from stocks_list import STOCKS

mas = MultiAsset()
mas.load('mqtest.txt', 1440)


params = load_settings_from_report('_PROBLEM.txt')

for s in STOCKS:

    c = mas.assets[s]
    c.set_to_last()
    cc = c.get()

    t = TS.open(cc, c, [], params)

    if t:
        print (s, t)
