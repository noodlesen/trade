import pandas as pd
from stockstats import StockDataFrame
from candlesticks import Candle, Figure
from reader import read_mt_csv

class Asset():

    def __init__(self, **kwargs):
        self.data = []# pd.DataFrame()
        self.symbol = kwargs.get('symbol', None)
        self.timeframe = kwargs.get('timeframe', None)
        self.pointer = 0
        self.count = 0
        self.range_from = 0
        self.range_to = None # first that is not in range

    def load_mt4_history(self, path, symbol, timeframe=1440):
        
        names = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        self.data = read_mt_csv(path, symbol, timeframe)
        self.symbol = symbol
        self.timeframe = timeframe
        #self.data = pd.read_csv(path, names=names, index_col=['date_time'], parse_dates=[['date','time']])
        # self.data = pd.read_csv(path, names=names)
        # self.data.set_index(['date', 'time'], drop=False)
        # self.stock = StockDataFrame(self.data)
        # self.data['value'] = self.data['open'] - self.data['close']
        # self.count = self.data.shape[0]
        self.reset_range()

    # def require(self, alpha):
    #     for a in alpha:
    #         x = self.stock[a]

    def reset(self):
        self.pointer = self.range_from

    def reset_range(self):
        self.range_from = 0
        self.range_to = self.count - 1
        self.range = self.range_to - self.range_from + 1

    def range_from_last(self, n):
        self.range_from = self.range - n - 1
        self.range_to = self.count - 1
        self.range = self.range_to - self.range_from + 1

    def set(self, n):
        self.pointer = n

    def forth(self, n=1):
        self.pointer += n

    def back(self, n=1):
        self.pointer -= n

    def next(self):
        self.pointer += 1

    def prev(self):
        self.pointer -= 1

    def last(self, n, of=0, **kwargs):
        of = abs(of)
        row = []
        fr = -1*(n-1)-of+self.pointer
        to = 1-of+self.pointer



        row = self.data[fr:to]


        if kwargs.get('figure', False):
            return Figure(candles=row)
        else:
            return row  
            

    # get bar by absoute index
    def bar(self, n=-1): 
        p = n if n >= 0 else self.pointer
        #return Candle(bar = dict(self.data.iloc[p]))
        return Candle(bar=self.data[p])

    # get bar by pointer relative index
    def get(self, n=0):
        #return Candle(bar = dict(self.data.iloc[self.pointer + n]))
        return Candle(bar=self.data[self.pointer + n])

    # def alpha(self, a, n=-1):
    #     p = n if n>=0 else self.pointer
    #     try:
    #         res = self.data.iloc[p][a]
    #     except KeyError:
    #         self.require([a])
    #         res = self.data.iloc[p][a]
    #     return res




# usdjpy = Asset()
# usdjpy.load_mt4_history('MTDATA','USDJPY', 60)
# usdjpy.require(['cci_2', 'cci_20'])
# print(usdjpy.data[usdjpy.data.value>0][['value']])
