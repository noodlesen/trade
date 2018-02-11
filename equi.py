from reader import read_mt_csv

symbols = ['USDJPY', 'USDCHF', 'EURUSD', 'CHFJPY', 'EURJPY', 'GBPJPY', 'GBPUSD']

data = {}

for s in symbols:
    d = read_mt_csv('DATA', s, 60)#[-20000:]
    data[s] = d
