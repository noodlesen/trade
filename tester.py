# TESTING TRADING STRATEGY OVER HISTORICAL DATA

from trading import get_trades_stats
from config import TS
from time import sleep


def test(c, params, **kwargs):
    trades = []
    c.reset()

    last_cc = None

    for i in range(c.range_from, c.range_to):
        cc = c.get()
        last_cc = cc
        TS.manage(cc, c, trades, params)
        trade = TS.open(cc, c, trades, params)
        if trade:
            trades.append(trade)

        c.next()

    for t in trades:
        if t.is_open and not t.is_closed:
            t.close_trade(last_cc, last_cc.close_price, 'FORCE_END')



    return get_trades_stats(trades, **kwargs)
