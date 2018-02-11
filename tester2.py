# TESTING TRADING STRATEGY OVER HISTORICAL DATA
from termcolor import colored, cprint
from random import randint

from candlesticks import Candle, Figure
from trading import Trade, get_trades_stats

#from ts_outlet import TS.manage, TS.open
from config import TS# TS.manage, TS.open



VERBOSE = False
HALT = False


def report(s):
    if VERBOSE:
        print(s)
    if HALT:
        input()



def test(c, params, **kwargs):

    #make_images = kwargs.get('draw', False)
    #verbose = kwargs.get('verbose', False)

    trades=[]

    c.reset()
    
    # <- TESTER LOOP
    for i in range(c.range_from, c.range_to):
        #print(i)

        # if i%50==0:
        #     print(i)

        cc = c.get()

        # CHECK EXISTING
        

                
        #
        # CHECK FOR OPEN
        #

       

        TS.manage(cc,c,trades, params)    
        trade = TS.open(cc,c, trades, params)
        if trade:
            trades.append(trade)
        c.next()

        # END OF TESTER LOOP

    #print ('loop finished')
    return get_trades_stats(trades, c, params, **kwargs)
