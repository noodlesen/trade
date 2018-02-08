from trading import Trade

def TS_manage(cc, c, trades, params):
    for trade in trades:
        if trade.is_open:

            trade.update_trade(cc)

            if not trade.is_closed:
                tp_base  = sum([d['high'] for d in trade.data])/len(trade.data)
                trade.takeprofit = tp_base*params.get('tp_koef', 2.1)

            # FIA — low profit - good winrate
            if params.get('use_FIA', False):
                fia_dmin = params.get('fia_dmin', 5)
                fia_dmax = params.get('fia_dmax', 15)
                fia_treshold = params.get('fia_treshold', 0.1)
                if trade.days > fia_dmin and trade.days < fia_dmax and (trade.profit/trade.days)/trade.open_price*100 < fia_treshold and trade.profit > 0:
                    trade.close_trade(cc, cc.close_price, 'FIA')

            #BREAKEVEN
            if not trade.is_closed and trade.stoploss<trade.open_price and cc.low_price>trade.open_price:
                if params.get('use_BREAKEVEN', False):
                    trade.stoploss = cc.low_price

            #FORCE TAKE PROFIT
            if not trade.is_closed and (trade.profit/trade.days)/trade.open_price>params.get('FTP',0.01):
                if params.get('use_FTP', False):
                    trade.close_trade(cc, cc.close_price, 'FTP')

            # PULL TO HAMMER/DOJI/SHOOTING STAR
            pull = False
            if not trade.is_closed:

                if cc.is_hammer():
                    if params.get('use_PTH', False):
                        pth = params.get('pth_mix', 0.25)
                        nsl = trade.stoploss*pth+cc.low_price*(1-pth)
                        pull = True

                if cc.is_shooting_star():
                    if params.get('use_PTSS', False):
                        ptss = params.get('ptss_mix', 0.25)
                        nsl = trade.stoploss*ptss+cc.low_price*(1-ptss)
                        pull = True

                if cc.is_doji():
                    if params.get('use_PTDJ', False):
                        ptdj = params.get('ptdj_mix', 0.25)
                        nsl = trade.stoploss*ptdj+cc.low_price*(1-ptdj)
                        pull = True

            if c.pointer>5 and params.get('use_PTTF', False):
                f = c.last(5)
                if f.is_top_fractal():
                    ptf = params.get('pttf_mix', 0.25)
                    nsl = trade.stoploss*ptf+cc.low_price*(1-ptf)
                    pull = True

            if c.pointer>5 and params.get('use_PTBF', False):
                f = c.last(5)
                if f.is_bottom_fractal():
                    ptf = params.get('ptbf_mix', 0.25)
                    nsl = trade.stoploss*ptf+cc.low_price*(1-ptf)
                    pull = True


            if pull:
                if nsl > trade.stoploss:
                    trade.stoploss = nsl


def TS_open(cc, c, trades, params):
    has_buy_signal = False
    has_sell_signal = False
    open_reason = None
    trade = None

    # TAIL
    #c = Candle(**d)
    bs = 0.01 if cc.body_size()==0 else cc.body_size()
    if cc.low_tail()/bs>0.2:
        has_buy_signal = True
        open_reason = 'TAIL'

    if c.pointer>5:
        # BREAKUP
        f = c.last(5)
        if f.is_breakup():
            has_buy_signal = True
            open_reason = 'B_UP'

        #HAMMER
        f = c.last(3)
        if f.summary().is_hammer() or f.summary(last=2).is_hammer():
            has_buy_signal = True
            open_reason = 'HAM'

        #FRACTAL
        f = c.last(5)
        if f.is_bottom_fractal():
            has_buy_signal = True
            open_reason = 'FRAC'


    if has_buy_signal or has_sell_signal:
        trade = Trade()
        if params.get('use_REL_TP', False):
            tp_value = cc.close_price*params.get('rel_tp_k', 0.2)
        else:
            tp_value = params.get('init_tp',50)
        if has_buy_signal:
            trade.open_trade('BUY', cc, cc.close_price, cc.low_price*params.get('init_sl_k',0.98), cc.close_price +tp_value, open_reason) 
        if has_sell_signal:
            trade.open_trade('SELL', cc, cc.close_price, cc.high_price*(2-params.get('init_sl_k',0.98)), cc.close_price -tp_value, open_reason) 

    return trade


