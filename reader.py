import json


def load_settings_from_report(path):
    with open(path,'r') as f:
        return json.loads(f.read())['input']


def read_nasdaq_csv(sym, cut=0):
    with open('data/'+sym+'.csv', 'r') as f:
        csv = f.read()

    lines = [l for l in csv.split('\n')]
    header = lines[0].split(',')
    lines = lines[1:]

    lines.reverse()

    data=[]


    for l in lines:
        nd = {}
        i = 0
        for n in l.split(','):
            h = header[i]
            if h == 'date':
                nd[h] = '/'.join(n[2:].split('-'))  # [::-1])
            else:
                nd[h] = int(float(n)*100)/100
            i += 1
        data.append(nd)
        #print(nd)

    if cut==0:
        return data
    else:
        return data[-cut:]



def read_mt_csv(sym, **kwargs):

    timeframe = kwargs.get('timeframe', 1440)

    slice_from = kwargs.get('slice_from',0)
    slice_to = kwargs.get('slice_to', 0)

    #print(slice_from, slice_to)
    #input()

    if slice_from == 0 and slice_to == 0:
        cut = kwargs.get('cut', 0)

    with open('MTDATA/'+sym+str(timeframe)+'.csv', 'r') as f:
        csv = f.read()

    lines = [l for l in csv.split('\n')][:-1]
    
    data=[]
    header = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']

    for l in lines:
        nd = {}
        i = 0
        for n in l.split(','):
            h = header[i]
            if h == 'date':
                nd[h] = n
            elif h == 'time':
                nd[h] = n
            elif h == 'volume':
                nd[h] = int(n)
            else:
                nd[h] = float(n)
            i += 1
        data.append(nd)

    if slice_from or slice_to:

        return data[slice_from: slice_to]
    elif cut==0:
        return data
    else:
        return data[-cut:]