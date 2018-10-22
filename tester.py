# TESTING TRADING STRATEGY OVER HISTORICAL DATA

from trading import get_trades_stats
from config import TS
from time import sleep


def test(c, params, **kwargs):
    trades = []
    c.reset()

    last_cc = None

    total_inv = 0
    max_dd = 0
    for i in range(c.range_from, c.range_to):
        cc = c.get()
        last_cc = cc
        TS.manage(cc, c, trades, params)
        trade = TS.open(cc, c, trades, params)
        if trade:
            trades.append(trade)
            total_inv+=trade.open_price

        cdd = sum([t.profit for t in trades if t.profit])
        if cdd<max_dd:
            max_dd =cdd

        c.next()

    for t in trades:
        if t.is_open and not t.is_closed:
            t.close_trade(last_cc, last_cc.close_price, 'FORCE_END')



    ts = get_trades_stats(trades, **kwargs)
    ts['TOTAL_INV'] = total_inv
    ts['ROI'] = ts['PROFIT']/total_inv
    ts['DD'] = max_dd
    return ts
