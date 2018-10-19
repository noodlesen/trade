from candlesticks import Candle, Figure
from reader import read_mt_csv


class Asset():

    def __init__(self, **kwargs):
        self.data = kwargs.get('data', [])
        self.symbol = kwargs.get('symbol', None)
        self.timeframe = kwargs.get('timeframe', None)
        self.pointer = 0
        self.range_from = 0
        self.count = len(self.data)
        self.range_to = self.count-1

    def load_mt4_history(self, path, symbol, timeframe=1440):
        self.data = read_mt_csv(path, symbol, timeframe)
        self.symbol = symbol
        self.timeframe = timeframe
        self.count = len(self.data)
        self.reset_range()

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


class MultiAsset():

    def __init__(self):
        self.assets = {}

    def load(self, symbol, timeframe):
        a = Asset()
        a.load_mt4_history('MTDATA', symbol, timeframe)
        self.assets[symbol] = a

    def show(self):
        for k, v in self.assets.items():
            print(v.symbol, v.count)



