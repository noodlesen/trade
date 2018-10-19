from candlesticks import Candle, Figure
from reader import read_mt_csv
import datetime

class Timeline():
    def __init__(self):
        self.data = []
        self.pointer = 0
        self.range_from = 0
        self.count = len(self.data)
        self.range_to = self.count-1

    def reset(self):
        self.pointer = self.range_from

    def set_to_last(self):
        self.pointer = self.range_to

    def reset_range(self):
        self.range_from = 0
        self.range_to = self.count - 1
        self.range = self.range_to - self.range_from + 1
        self.pointer = 0

    def range_from_last(self, n):
        self.range_from = self.count - n - 1
        self.range_to = self.count - 1
        self.range = self.range_to - self.range_from + 1
        self.pointer = self.range_from

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



class Asset(Timeline):

    def __init__(self, **kwargs):
        self.data = kwargs.get('data', [])
        self.symbol = kwargs.get('symbol', None)
        self.timeframe = kwargs.get('timeframe', None)


    def load_mt4_history(self, path, symbol, timeframe=1440):
        self.data = read_mt_csv(path, symbol, timeframe)
        self.symbol = symbol
        self.timeframe = timeframe
        self.count = len(self.data)
        self.reset_range()

    

    def last(self, n, of=0, **kwargs):
        of = abs(of)
        row = []
        fr = -1*(n-1)-of+self.pointer
        to = 1-of+self.pointer
        row = self.data[fr:to]
        if kwargs.get('figure', False):
            return Figure(raw=row)
        else:
            return row

    # get bar by absoute index
    def bar(self, n=-1):
        p = n if n >= 0 else self.pointer
        return Candle(bar=self.data[p])

    # get bar by pointer relative index
    def get(self, n=0):
        return Candle(bar=self.data[self.pointer + n])


# class MultiAsset(Asset): ### СДЕЛАТЬ единым массивом

#     def __init__(self):
#         self.assets = {}

#     def load(self, symbol, timeframe):
#         a = Asset()
#         a.load_mt4_history('MTDATA', symbol, timeframe)
#         self.assets[symbol] = a

#     def show(self):
#         for k, v in self.assets.items():
#             print(v.symbol, v.count)
#             print(datetime.datetime.strptime(v.get().date, '%Y.%m.%d'))
#             v.set_to_last()
#             print(datetime.datetime.strptime(v.get().date, '%Y.%m.%d')) # --> перенести в Candle

#     def join(self):
#         newest_start = datetime(day=1, month=1, year=1900)
#         latest_finish = datetime.today()
#         for k, v in self.assets.items():
#             dt = datetime.datetime.strptime(v.get().date, '%Y.%m.%d')
#             if dt > 

class MultiAsset(Asset):

    def __init__(self):
        self.data = []
        self.symbol = 'MULTI'
        self.symbols = []
        self.raw_data = {}

    def load_mt4_history(self, path, symbol, timeframe=1440):
        self.raw_data[symbol] = read_mt_csv(path, symbol, timeframe)
        self.symbols.append(symbol)
        self.timeframe = timeframe
        self.count = len(self.data)
        self.reset_range()

    def show(self):
        print (self.symbols)
        for k,v in self.raw_data.items():
            print(k, len(v))

