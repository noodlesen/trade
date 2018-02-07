import pandas as pd
from stockstats import StockDataFrame
from candlesticks import Candle

class Asset():

    def __init__(self, **kwargs):
        self.data = pd.DataFrame()
        self.symbol = kwargs.get('symbol', None)
        self.timeframe = kwargs.get('timeframe', None)
        self.pointer = 0

    def load_mt4_history(self, path, symbol, timeframe):
        if path[-1]!='/':
            path+='/'
        path+=symbol+str(timeframe)+'.csv'
        names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        #self.data = pd.read_csv(path, names=names, index_col=['date_time'], parse_dates=[['date','time']])
        self.data = pd.read_csv(path, names=names)
        self.data.set_index(['date', 'time'], drop=False)
        self.stock = StockDataFrame(self.data)
        self.data['value']=self.data['open'] - self.data['close']

    def require(self, indis):
        for ind in indis:
            x = self.stock[ind]

    def reset(self):
        self.pointer = 0

    def set(self, n):
        self.pointer = n

    def get(self, n=-1):
        p = n if n>=0 else self.pointer
        return Candle(bar = dict(self.data.iloc[p]))

    def alpha(self, a, n=-1):
        p = n if n>=0 else self.pointer
        try:
            res = self.data.iloc[p][a]
        except KeyError:
            self.require([a])
            res = self.data.iloc[p][a]
        return res




usdjpy = Asset()
usdjpy.load_mt4_history('MTDATA','USDJPY', 60)
usdjpy.require(['cci_2', 'cci_20'])
print(usdjpy.data[usdjpy.data.value>0][['value']])
