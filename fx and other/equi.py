from reader import read_mt_csv
from drawer import draw_plot, draw_candles
import math

symbols = ["USDJPY", "USDCHF", "EURUSD", "CHFJPY", "EURJPY", "GBPJPY", "GBPUSD"]

data = {}

for s in symbols:
    d = read_mt_csv('DATA', s, 60)[-20000:]
    data[s] = d

last = 0
rys=[]
last_res = [0,0,0]
deltas = [[],[],[]]
for i in range(0, 50):
    ty = round(data['USDJPY'][i]['close']+data['EURJPY'][i]['close']+data['CHFJPY'][i]['close']+data['GBPJPY'][i]['close']+1, 3)
    td = round(data['EURUSD'][i]['close']+data['GBPUSD'][i]['close']+1/data['USDCHF'][i]['close']+1/data['USDJPY'][i]['close']+1, 5)
    ry = data['USDJPY'][i]['close']
    ny = round(ty/td, 3)
    yd = round(ty/td-ry, 3)

    res = [ry, ty, td]
    rys.append(ry)
    print (res)
    for x in range(0,3):
        if i>0:
            dt = round((res[x]-last_res[x])/last_res[x]*100, 6)
        else:
            dt=0
        print(dt)
        deltas[x].append(dt)
    last_res = res
    last = yd

#print (deltas[0][-300:])
draw_plot(deltas, 'test')
draw_candles(data['USDJPY'][0:50], 'candles', {'width':1920, 'height':800, "number":50, "offset": 0})