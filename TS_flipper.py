from trading import Trade, trade_stats, close_all
from random import randint, choice
from indi import CCI, EMA

print ('FLIPPER HERE')


def manage(cc, c, trades, params):
    for trade in trades:
        if trade.is_open:
            trade.update_trade(cc)

            if not trade.is_closed:
                if trade.direction == 'BUY':
                    tp_base  = sum([d['high'] for d in trade.data])/len(trade.data)
                    trade.takeprofit = tp_base*params.get('tp_koef', 2.1)
                elif trade.direction == 'SELL':
                    tp_base  = sum([d['low'] for d in trade.data])/len(trade.data)
                    trade.takeprofit = tp_base*1/params.get('tp_koef', 2.1)

            # FIA — low profit - good winrate
            if params.get('use_FIA', False):
                fia_dmin = params.get('fia_dmin', 5)
                fia_dmax = params.get('fia_dmax', 15)
                fia_treshold = params.get('fia_treshold', 0.1)
                if trade.days > fia_dmin and trade.days < fia_dmax and (trade.profit/trade.days)/trade.open_price*100 < fia_treshold and trade.profit > 0:
                    trade.close_trade(cc, cc.close_price, 'FIA')

            #BREAKEVEN
            if not trade.is_closed and params.get('use_BREAKEVEN', False):
                if trade.direction == 'BUY' and trade.stoploss<trade.open_price and cc.low_price>trade.open_price:
                    trade.stoploss = cc.low_price
                if trade.direction == 'SELL' and trade.stoploss>trade.open_price and cc.high_price<trade.open_price:
                    trade.stoploss = cc.high_price

            #FORCE TAKE PROFIT
            if not trade.is_closed and params.get('use_FTP', False):
                if (trade.profit/trade.days)/trade.open_price>params.get('FTP',0.01):
                    trade.close_trade(cc, cc.close_price, 'FTP')

            if not trade.is_closed:
                ema = EMA(c.last(12), 5)
                if trade.direction == 'BUY':
                    if cc.close_price > ema:
                        trade.close_trade(cc, cc.close_price, 'EMA_CROSS')

                if trade.direction == 'SELL':
                    if cc.close_price < ema:
                        trade.close_trade(cc, cc.close_price, 'EMA_CROSS')
                    


   


def open(cc, c, trades, params):

    trade = None

    ts = trade_stats(trades)

    allowed_to_buy = False
    allowed_to_sell = False

    has_buy_signal = False
    has_sell_signal = False
    open_reason = None

    if ts['open'] <= params.get('max_pos',50):    

        ema = EMA(c.last(12), 5)
        pema = EMA(c.last(12,1), 5)


        g2 = ema - c.get(0).high_price
        if g2>0:
            has_buy_signal = True

        g2 = c.get(0).low_price - ema
        if g2>0:
            has_sell_signal = True

        if (has_buy_signal or has_sell_signal):
            trade = Trade()
            
            tp_value = cc.close_price*params.get('init_tp_k', 0.2)
 


            if has_buy_signal:
                if ts['open_long'] > ts['open_short'] or ts['open']==0:
                    allowed_to_buy = True
                else:
                    if ts['open_profit']>params.get('flip_th', 0)*cc.close_price:
                        pass
                        if params.get('use_FLIP', False):
                            close_all(trades, cc, 'FLIP')
                            allowed_to_sell = True

            if has_sell_signal:
                if ts['open_long'] < ts['open_short'] or ts['open']==0:
                    allowed_to_sell = True
                else:
                    if ts['open_profit']>params.get('flip_th', 0)*cc.close_price:
                        pass
                        if params.get('use_FLIP', False):
                            close_all(trades, cc, 'FLIP')
                            allowed_to_buy = True

            if allowed_to_buy and allowed_to_sell:
                allowed_to_buy = False
                allowed_to_sell = False
                
            if allowed_to_buy:
                trade.open_trade('BUY', cc, cc.close_price, cc.low_price*params.get('init_sl_k',0.98), cc.close_price +tp_value, open_reason)

            if allowed_to_sell:
                trade.open_trade('SELL', cc, cc.close_price, cc.high_price*(2-params.get('init_sl_k',0.98)), cc.close_price -tp_value, open_reason) 


    return trade


def get_random_params():
    params = {
        'tp_koef': randint(1,40)/10,
        'use_FIA': choice([True, False]),
        'use_BREAKEVEN': choice([True, False]),
        'use_FTP': choice([True, False]),
        'fia_dmin': randint(2,5),
        'fia_dmax': randint(5,12),
        'fia_treshold': randint(1,2000)/10000,
        'init_sl_k': randint(9899,9999)/10000,
        'FTP': randint(1,3000)/10000,
        'init_tp_k': randint(5,1000)/1000,
        'use_FLIP': choice([True, False]),
        'flip_th': randint(-100,100)/1000

    }
    
    params['max_pos'] = 3
    #params['trade_short'] = True
    return params



