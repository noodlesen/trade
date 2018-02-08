# TESTING TRADING STRATEGY OVER HISTORICAL DATA
from termcolor import colored, cprint
from random import randint
from drawer import draw_candles
from candlesticks import Candle, Figure



VERBOSE = False
HALT = False


def report(s):
    if VERBOSE:
        print(s)
    if HALT:
        input()


class Trade():

    def __str__(self):
        return '%s | %r > %r | = %r [%s]' % (self.direction, self.open_price, self.close_price, self.profit, self.close_reason)

    def __init__(self):
        self.open_price = None
        self.close_price = None
        self.stoploss = None
        self.takeprofit = None
        self.days = 0
        self.data = []
        self.low = None
        self.high = None
        self.open_date = None
        self.close_date = None
        self.profit = None
        self.open_reason = None
        self.close_reason = None

        self.direction = None

        self.is_open = False
        self.is_closed = False


    def open_trade(self, direction, daydata, price, stoploss, takeprofit, open_reason):
        self.direction = direction
        self.days += 1
        self.is_open = True
        self.open_price = price
        self.open_reason = open_reason
        self.stoploss = stoploss
        self.takeprofit = takeprofit
        dd = daydata.get_dict()
        dd['stoploss'] = stoploss
        dd['takeprofit'] = takeprofit
        self.data.append(dd)
        self.low = daydata.close_price
        self.high = daydata.close_price
        self.open_date = daydata.date
        self.open_time = daydata.time
        report('OPEN: '+self.__str__()+' SL:'+str(self.stoploss))

    def close_trade(self, daydata, price, close_reason):
        self.close_price = price
        self.close_date = daydata.date
        self.close_time = daydata.time

        delta = round(self.close_price - self.open_price, 2)
        if self.direction:
            if self.direction == 'BUY':
                self.profit = delta
            elif self.direction == 'SELL':
                self.profit = -1*delta

        self.is_open = False
        self.is_closed = True
        self.close_reason = close_reason
        report('CLOSE: '+self.__str__()+' SL:'+str(self.stoploss))

    def update_trade(self, daydata):
        self.days += 1

        dd = daydata.get_dict()
        dd['stoploss'] = self.stoploss
        dd['takeprofit'] = self.takeprofit
        self.data.append(dd)

        if daydata.high_price > self.high:
            self.high = daydata.high_price
        if daydata.low_price < self.low:
            self.low = daydata.low_price

        if self.direction == 'BUY':

            if daydata.low_price <= self.stoploss:
                self.close_trade(daydata, self.stoploss, 'SL')
            if daydata.high_price >= self.takeprofit:
                self.close_trade(daydata, self.takeprofit, 'TP')

            if not self.is_closed:
                self.profit = daydata.close_price - self.open_price


        elif self.direction == 'SELL':

            if daydata.high_price >= self.stoploss:
                self.close_trade(daydata, self.stoploss, 'SL')
            if daydata.low_price <= self.takeprofit:
                self.close_trade(daydata, self.takeprofit, 'TP')

            if not self.is_closed:
                self.profit = self.open_price - daydata.close_price






def test(c, params, **kwargs):

    make_images = kwargs.get('draw', False)
    verbose = kwargs.get('verbose', False)

    trades=[]
    open_trades_stats =[]

    c.reset()
    
    # <- TESTER LOOP
    for i in range(c.range_from, c.range_to):

        cc = c.get()
        open_trades = 0

        # CHECK EXISTING
        for trade in trades:
            if trade.is_open:
                open_trades+=1
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

                # #CUTTER
                # if not trade.is_closed and params.get('use_CUT', False):
                #     cut_period = params.get('cut_period', 3)
                #     cut_treshold = params.get('cut_treshold', 0.001)
                #     cut_mix = params.get('cut_mix', 0.75)
                #     if i>cut_period:
                #         s = sum([dd['close']-dd['open'] for dd in data[i-cut_period:i]])
                #         sop = s/cut_period/trade.open_price
                        
                #         if sop<cut_treshold:
                #             nsl = d['low']*cut_mix+trade.stoploss*(1-cut_mix)
                #             if nsl>trade.stoploss:
                #                 trade.stoploss=nsl

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
                    # c = Candle(**cc)

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

                if i>5 and params.get('use_PTTF', False):
                    f = c.last(5) #Figure(raw=data[i-5:i+1])
                    if f.is_top_fractal():
                        ptf = params.get('pttf_mix', 0.25)
                        nsl = trade.stoploss*ptf+cc.low_price*(1-ptf)
                        pull = True

                if i>5 and params.get('use_PTBF', False):
                    f = c.last(5)#Figure(raw=data[i-5:i+1])
                    if f.is_bottom_fractal():
                        ptf = params.get('ptbf_mix', 0.25)
                        nsl = trade.stoploss*ptf+cc.low_price*(1-ptf)
                        pull = True


                if pull:
                    if nsl > trade.stoploss:
                        trade.stoploss = nsl

                
        #
        # CHECK FOR OPEN
        #

        has_buy_signal = False
        has_sell_signal = False
        open_reason = None

        # TAIL
        #c = Candle(**d)
        bs = 0.01 if cc.body_size()==0 else cc.body_size()
        if cc.low_tail()/bs>0.2:
            has_buy_signal = True
            open_reason = 'TAIL'

        if i>5:
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

        filter_passed = True

        # if params.get('use_FILTERS', False):
        #     filter_passed = False
        #     max_per = params.get('f_max_per', 250)
        #     th = params.get('f_max_th', 0.8)
        #     if i>max_per:
        #         #m = max([dd['high'] for dd in data[i-max_per:i+1]])
        #         #m = c.alpha('high_%s~0_max' % str(max_per))
        #         m = c.last(max_per).summary().high_price
        #         if cc.close_price > m*th:
        #             filter_passed = True

        if filter_passed and (has_buy_signal or has_sell_signal):
            trade = Trade()
            if params.get('use_REL_TP', False):
                tp_value = cc.close_price*params.get('rel_tp_k', 0.2)
            else:
                tp_value = params.get('init_tp',50)
            if has_buy_signal:
                trade.open_trade('BUY', cc, cc.close_price, cc.low_price*params.get('init_sl_k',0.98), cc.close_price +tp_value, open_reason) 
            if has_sell_signal:
                trade.open_trade('SELL', cc, cc.close_price, cc.high_price*(2-params.get('init_sl_k',0.98)), cc.close_price -tp_value, open_reason) 
            trades.append(trade)

        open_trades_stats.append(open_trades)
        c.next()

        # END OF TESTER LOOP


    #=========================================#
    #                                         #
    #       STATS AND OUTPUT                  #
    #                                         #
    #=========================================#
    n = 1
    s = 0

    days_max = 0
    days_min = 10000000
    number_of_wins = 0
    number_of_loses = 0
    max_loses_in_a_row = 0
    max_wins_in_a_row = 0
    current_loses_in_a_row = 0
    current_wins_in_a_row = 0
    sum_of_wins = 0 
    sum_of_loses = 0
    max_profit_per_trade = 0
    max_loss_per_trade = 0


    open_reasons ={}
    close_reasons={}

    i = 0
    for t in trades:
        if t.is_closed:
            i+=1

            if t.open_reason in open_reasons.keys():
                open_reasons[t.open_reason][0]+=1
                open_reasons[t.open_reason][1]+=t.profit
            else:
                open_reasons[t.open_reason]=[0,0]


            if t.close_reason in close_reasons.keys():
                close_reasons[t.close_reason][0]+=1
                close_reasons[t.close_reason][1]+=t.profit
            else:
                close_reasons[t.close_reason]=[0,0]

            if make_images:
                context = {
                    'number':len(t.data),
                    'width': 1000,
                    'height': 500,
                    'offset': 0
                }
                draw_candles(t.data, 'images/'+c.symbol+str(i)+'_'+t.direction+'_'+t.close_reason, context)


            if t.days>days_max:
                days_max = t.days
            if t.days<days_min:
                days_min = t.days

            if t.profit<0:
                if verbose:
                    print(colored(t, 'red'))
                number_of_loses+=1
                current_loses_in_a_row +=1
                if current_wins_in_a_row>max_wins_in_a_row:
                    max_wins_in_a_row = current_wins_in_a_row
                current_wins_in_a_row = 0
                sum_of_loses += t.profit
                if t.profit<max_loss_per_trade:
                    max_loss_per_trade = t.profit

            else:
                if verbose:
                    print(t)
                number_of_wins+=1
                current_wins_in_a_row +=1
                if current_loses_in_a_row>max_loses_in_a_row:
                    max_loses_in_a_row = current_loses_in_a_row
                current_loses_in_a_row = 0
                sum_of_wins += t.profit
                if t.profit>max_profit_per_trade:
                    max_profit_per_trade = t.profit




    number_of_trades = len(trades)
    if number_of_loses:
        average_loss = sum_of_loses/number_of_loses
    else:
        average_loss = 0

    if number_of_wins:
        average_win = sum_of_wins/number_of_wins
    else:
        average_win = 0

    res = {}
    res['SYMBOL'] = c.symbol
    res['PROFIT'] = sum_of_wins+sum_of_loses
    res['TRADES'] = number_of_trades
    res['WINS'] = number_of_wins
    res['LOSES'] = number_of_loses
    res['WINS_TO_LOSES'] = number_of_wins/number_of_loses if number_of_loses > 0 else None
    res['WINRATE'] = number_of_wins/number_of_trades if number_of_trades > 0 else None
    res['AVG_WIN'] = average_win
    res['AVG_LOSS'] = average_loss
    res['MAX_PROFIT_PER_TRADE'] = max_profit_per_trade
    res['MAX_LOSS_PER_TRADE'] = max_loss_per_trade
    res['MAX_WINS_IN_A_ROW'] = max_wins_in_a_row
    res['MAX_LOSES_IN_A_ROW'] = max_loses_in_a_row
    res['DAYS_MAX'] = days_max
    res['DAYS_MIN'] = days_min
    res['OPEN_REASONS'] = open_reasons
    res['CLOSE_REASONS'] = close_reasons

    return res
