# TESTING TRADING STRATEGY OVER HISTORICAL DATA
from termcolor import colored, cprint
from random import randint

from candlesticks import Candle, Figure
from trading import Trade, get_trades_stats

from TS_follower import TS_manage, TS_open



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
    open_trades_stats =[]

    c.reset()
    
    # <- TESTER LOOP
    for i in range(c.range_from, c.range_to):

        cc = c.get()

        # CHECK EXISTING
        

                
        #
        # CHECK FOR OPEN
        #

       

        TS_manage(cc,c,trades, params)    
        trade = TS_open(cc,c, trades, params)
        if trade:
            trades.append(trade)
        c.next()

        # END OF TESTER LOOP

    return get_trades_stats(trades, c, params, draw=True)
