from evo import generate, get_random_params
from tester import trading_system
from reader import read_mt_csv
from termcolor import colored, cprint
from drawer import draw_candles

#generate(['BA'], 300, 4, 5, 10, 'MAX_PROFIT')

initial_params = {
        "FTP": 0.0438,
        "cut_mix": 0.3,
        "cut_period": 19,
        "cut_treshold": 0.028,
        "fia_dmax": 10,
        "fia_dmin": 2,
        "fia_treshold": 0.07,
        "init_sl_k": 0.93,
        "init_tp": 5,
        "ptdj_mix": 0.07,
        "ptf_mix": 0.36,
        "pth_mix": 0.27,
        "ptss_mix": 0.14,
        "rel_tp_k": 0.51,
        "tp_koef": 1.2,
        "use_BREAK": False,
        "use_BREAKEVEN": False,
        "use_CUT": False,
        "use_FIA": True,
        "use_FTP": True,
        "use_GAP": False,
        "use_PTDJ": True,
        "use_PTH": False,
        "use_PTSS": False,
        "use_REL_TP": False
    }


def simulate(symbol, data, initial_params, **kwargs):

    make_images = kwargs.get('draw', False)
    verbose = kwargs.get('verbose', False)

    if verbose:
        print('SIMULATION STARTED')

    params = initial_params

    opt_per = 100

    test_per = 250

    i = test_per+1
    trades=[]
    open_trades_stats =[]

    for d in data[test_per+1:-1]:
        print('I: ',i)
        #if i%opt_per==0:
            # print('OPTIMIZING')
            # params = generate([symbol], 100, 3, 7, 12, 'EVERYTHING', slice_from=i-test_per, slice_to=i, initial_params=params)['input']
            # print('PARAMETERS HAS CHANGED')
        trades, ot = trading_system(data, i, trades, params)
        open_trades_stats.append(ot)
        i += 1


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
                draw_candles(t.data, 'images/'+symbol+str(i)+'_'+t.close_reason, context)


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
    res['SYMBOL'] = symbol
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

symbol = 'ADBE'
data = read_mt_csv(symbol, cut=2000, timeframe=1440)

res = simulate(symbol, data, get_random_params(), verbose=True, draw=True)

print (res)