from reader import read_mt_csv

symbols = ['USDJPY', 'USDCHF', 'EURUSD', 'CHFJPY', 'EURJPY', 'GBPJPY', 'GBPUSD']

data = {}

for s in symbols:
    d = read_mt_csv('DATA', s, 60)[-20000:]
    data[s] = d

last = 0
for i in range(0,20000):
    ty = data['USDJPY'][i]['close']+data['EURJPY'][i]['close']+data['CHFJPY'][i]['close']+data['GBPJPY'][i]['close']+1
    td = data['EURUSD'][i]['close']+data['GBPUSD'][i]['close']+1/data['USDCHF'][i]['close']+1/data['USDJPY'][i]['close']+1
    ry = data['USDJPY'][i]['close']
    ny = round(ty/td, 3)
    yd = round(ty/td-ry, 3) 

    print(ry, ny, yd )
    if last>0.01:
        input()
    last = yd