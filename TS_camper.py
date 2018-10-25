from trading import Trade #, close_all
from random import randint, choice
from indi import CCI

TS_NAME = 'CAMPER'

def ts_name():
    return (TS_NAME)

def manage(cc, c, trades, params):
    for trade in trades:
        trade.update_trade(cc)
        if trade.is_open:
            trade.close_trade(cc, cc.close_price, 'SHOT')



def open(cc, c, trades, params):

    trade = None

    #ts = trade_stats(trades)

    allowed_to_buy = False

    has_buy_signal = False

    open_reason = None

    if True:  #ts['open'] <= params.get('max_pos', 50):    

        # TAIL
        if params.get('open_TAIL', False):
            bs = 0.01 if cc.body_size() == 0 else cc.body_size()
            if cc.low_tail()/bs > 0.2:
                has_buy_signal = True
                open_reason = 'TAIL_BUY'


        if c.pointer > 5:

            # BREAKUP
            if params.get('open_BREAK', False):
                f = c.last(5, figure=True)
                if f.is_breakup():
                    has_buy_signal = True
                    open_reason = 'BREAKUP_BUY'

            #HAMMER
            if params.get('open_HAMMER', False):
                f = c.last(3, figure=True)
                if f.summary().is_hammer() or f.summary(last=2).is_hammer():
                    has_buy_signal = True
                    open_reason = 'HAMMER_BUY'

            #DOUBLE HAMMER
            if params.get('open_DOUBLE_HAMMER', False):
                pf = params.get('dh_fast', 2)
                ps = params.get('dh_slow', 20)

                if c.last(pf, figure=True).summary().is_hammer() and c.last(ps, figure=True).summary().is_hammer():
                    has_buy_signal = True
                    open_reason = 'DOUBLE_HAMMER'

            #FRACTAL
            if params.get('open_FRACTAL', False):
                f = c.last(5, figure=True)
                if f.is_bottom_fractal():
                    has_buy_signal = True
                    open_reason = 'FRAC_BUY'

        if params.get('open_C2', False):
            if CCI(c.last(2)) > CCI(c.last(2, -1)):
                has_buy_signal = True
                open_reason = 'C2_BUY'

        passed_filters = []

        if params.get('use_HIGH_FILTER', False):

            high_filter_passed = 0
            max_per = params.get('hf_max_per', 250)
            th = params.get('hf_max_th', 0.8)
            if c.pointer > max_per:
                m = max(bar['high'] for bar in c.last(max_per))
                if cc.close_price > m*th:
                    high_filter_passed = 1
            passed_filters.append(high_filter_passed)

        if params.get('use_CCI_FILTER', False):
            cci_filter_passed = 0
            per = params.get('cci_f_per', 14)
            if CCI(c.last(per)) > CCI(c.last(per, -1)):
                cci_filter_passed = 1     
            passed_filters.append(cci_filter_passed)


        all_filters_passed = sum(passed_filters) == len(passed_filters)


        if all_filters_passed and has_buy_signal:

            tp_value = cc.close_price*params.get('rel_tp_k', 0.2)

            if has_buy_signal:
                #if ts['open_long'] > ts['open_short'] or ts['open'] == 0:
                allowed_to_buy = True

            if allowed_to_buy:
                trade = Trade()
                trade.open_trade(c.symbol, 'BUY', cc, cc.close_price, cc.low_price*params.get('init_sl_k', 0.98), cc.close_price + tp_value, open_reason)

    return trade


def get_random_ts_params():
    params = {
        'init_sl_k': randint(500, 999)/1000,
        'dh_fast': randint(1, 5),
        'dh_slow': randint(8, 50),
        'FTP': randint(1, 3000)/10000,
        'use_HIGH_FILTER': choice([True, False]),
        'hf_max_per': randint(20, 301),
        'hf_max_th': randint(50, 95)/100,
        'open_C2': choice([True, False]),
        'open_FRACTAL': choice([True, False]),
        'open_HAMMER': choice([True, False]),
        'open_TAIL': choice([True, False]),
        'open_BREAK': choice([True, False]),
        'open_DOUBLE_HAMMER': choice([True, False]),
        'use_CCI_FILTER': choice([True, False]),
        'cci_f_per': randint(8,20)

    }

    params['max_pos'] = 100
    return params
