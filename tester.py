# TESTING TRADING STRATEGY OVER HISTORICAL DATA

from trading import get_trades_stats
from config import TS


def test(c, params, **kwargs):
    trades = []
    c.reset()

    for i in range(c.range_from, c.range_to):
        cc = c.get()
        TS.manage(cc, c, trades, params)
        trade = TS.open(cc, c, trades, params)
        if trade:
            trades.append(trade)
        c.next()

    return get_trades_stats(trades, c, params, **kwargs)
