# EVOLUTION ALGORITHM FOR TESTING

from random import randint
from copy import deepcopy
import json
from tester2 import test
from holder import Asset
from reader import read_mt_csv
from ts_outlet import get_random_params




def mutate(p,n):
    new_params = get_random_params()
    numbers = []
    l = len(p.items())
    n = randint(1,n)
    while len(numbers)<n:
        nn = randint(1,l)
        if nn not in numbers:
            numbers.append(nn)
    np = deepcopy(p)
    x = 1
    for k,v in new_params.items():
        if x in numbers:
            np[k]=new_params[k]
        x+=1
    return np



def test_all(assets, params, **kwargs):
    
    results = []
    for an, a in assets.items():
            #data = read_mt_csv(s, **kwargs)
            results.append(test(a, params, **kwargs))

    wins = sum([r['WINS'] for r in results])
    loses = sum([r['LOSES'] for r in results])
    trades = sum([r['TRADES'] for r in results])
    winrate =  wins/trades if trades > 0 else None
    wins_to_loses = wins/loses if loses > 0 else None
    output = {
        'PROFIT': sum([r['PROFIT'] for r in results]),
        'TRADES': trades,
        'WINS': wins,
        'LOSES': loses,
        'WINS_TO_LOSES': wins_to_loses,
        'WINRATE': winrate,
        'MAX_PROFIT_PER_TRADE': max([r['MAX_PROFIT_PER_TRADE'] for r in results]),
        'MAX_LOSS_PER_TRADE': max([r['MAX_LOSS_PER_TRADE'] for r in results]),
        'MAX_WINS_IN_A_ROW': max([r['MAX_WINS_IN_A_ROW'] for r in results]),
        'MAX_LOSES_IN_A_ROW': max([r['MAX_LOSES_IN_A_ROW'] for r in results]),
    }
    return {
        'ALL': output,
        'PASSES': results
    }


def generate(symbols, timeframe, generations_count, mutations, outsiders, depth, strategy, **kwargs):
    cut = kwargs.get('cut', False)
    assets = {}
    for s in symbols:
        a = Asset()
        a.load_mt4_history('MTDATA', s, timeframe)
        if cut:
            
            a.range_from_last(cut)
        assets[s] = a

    results = []
    tr = 0
    tries = 0
    while tr == 0:
        if tries:
            initial = get_random_params()
        else:
            initial = kwargs.get('initial_params', get_random_params())
        #
        initial_result = test_all(assets, initial, **kwargs)
        tr = initial_result['ALL']['TRADES']
        tries+=1
        #print(tries)
        #print('trades:', tr)
    survivor  = {'input': initial, 'output': initial_result}
    print(json.dumps(survivor['input'], sort_keys=True, indent=4))

    for n in range(0,generations_count):
        print('GEN', n)

        offs = []
        for d in range(0,depth):
            #print('depth', d)
            m = mutate(survivor['input'], mutations)
            offs.append({'input': m, 'output': test_all(assets, m, **kwargs)})

        for x in range(0, outsiders):
            #print('outsider', x)
            m = get_random_params()
            offs.append({'input': m, 'output': test_all(assets, m, **kwargs)})

        for off in offs:

            #print('off')

            if off['output']['ALL']['TRADES']>0:
                off_wr = (off['output']['ALL']['WINS'])/off['output']['ALL']['TRADES']
                survivor_wr = (survivor['output']['ALL']['WINS'])/survivor['output']['ALL']['TRADES']

                if strategy == 'PROFIT_AND_WINRATE':            
                    cond = off['output']['ALL']['PROFIT']*off_wr > survivor['output']['ALL']['PROFIT']*survivor_wr and off_wr>0.5

                elif strategy == 'MAX_PROFIT':
                    cond = off['output']['ALL']['PROFIT'] > survivor['output']['ALL']['PROFIT'] and off_wr>0.5

                elif strategy == 'EVERYTHING':
                    off_max_loses = off['output']['ALL']['MAX_LOSES_IN_A_ROW']
                    off_max_loses = 0.01 if off_max_loses == 0 else off_max_loses
                    sur_max_loses = survivor['output']['ALL']['MAX_LOSES_IN_A_ROW']
                    sur_max_loses = 0.01 if sur_max_loses == 0 else sur_max_loses
                    off_max_wins =  off['output']['ALL']['MAX_WINS_IN_A_ROW']
                    sur_max_wins =  survivor['output']['ALL']['MAX_WINS_IN_A_ROW']
                    #off_trades = off['output']['ALL']['TRADES']
                    #survivor_trades = survivor['output']['ALL']['TRADES']
                    cond = off['output']['ALL']['PROFIT']/off_max_loses*off_wr*off_max_wins > survivor['output']['ALL']['PROFIT']/sur_max_loses*survivor_wr*sur_max_wins

                if cond:
                    survivor = deepcopy(off)

        print(json.dumps(survivor['input'], sort_keys=True, indent=4))
        print('>>>>')
        print(survivor['output']['ALL']['WINS']/survivor['output']['ALL']['TRADES'])
        print(survivor['output']['ALL']['PROFIT'])
        print()


    if kwargs.get('report', False):
        with open('evo.txt', 'w') as f:
            # print(survivor)
            # input()
            f.write(json.dumps(survivor, sort_keys=True, indent=4))

        kwargs['draw'] = True
        kwargs['verbose'] = True
        test_all(assets, survivor['input'], **kwargs)

        print(json.dumps(survivor['output']['ALL'], sort_keys=True, indent=4))


    return(survivor)


