
class Indi():

    def __init__(self, data):
        self.data = data

    def check(self, max_period):
        return True if max_period >= len(self.data) else False

    def CCI(self, period):
        if self.check(period):
            for d in data:
                d['tp']=(d['high']+d['close']+d['low'])/3
            for i,d in enumerate(data):
                if i >= period:
                    pass
        else:
            return None

#####

import quandl



# Commodity Channel Index Python Code

# Load the necessary packages and modules
from pandas_datareader import data as pdr
import pandas as pd

# Commodity Channel Index 
def CCI(data, ndays): 
 TP = (data['High'] + data['Low'] + data['Close']) / 3 
 CCI = pd.Series((TP - TP.rolling(ndays).mean()) / (0.015 * TP.rolling(ndays).std()),
 name = 'CCI') 
 data = data.join(CCI) 
 return data

# Retrieve the Nifty data from Yahoo finance:
data = pd.read_csv('pd_aapl.csv', header=0, index_col='Date', parse_dates=True)

# Compute the Commodity Channel Index(CCI) for NIFTY based on the 20-day Moving average
n = 2
NIFTY_CCI = CCI(data, n)
CCI = NIFTY_CCI['CCI']

print(CCI)
