# DATA READING LIBRARY

import json
#from time import sleep


def load_settings_from_report(path):
    with open(path, 'r') as f:
        return json.loads(f.read())['input']


def read_av_json(path, symbol, **kwargs):
    slice_from = kwargs.get('slice_from', 0)
    slice_to = kwargs.get('slice_to', 0)

    if slice_from == 0 and slice_to == 0:
        cut = kwargs.get('cut', 0)

    if path[-1] != '/':
        path += '/'
    path += symbol + '.json'

    with open(path, 'r') as f:
        data = json.loads(f.read())["Time Series (Daily)"]

    datalist = [{k: data[k]} for k in sorted(data.keys())]


    data =[]
    for d in datalist:
        k = list(d.keys())[0]
        data.append(
            {
                "date": k,
                "time": '',
                "open": float(d[k]['1. open']),
                "high": float(d[k]['2. high']),
                "low": float(d[k]['3. low']),
                "close": float(d[k]['5. adjusted close']),
                "volume": int(d[k]['6. volume'])
            }
        )


    if slice_from or slice_to:

        return data[slice_from: slice_to]
    elif cut == 0:
        return data
    else:
        return data[-cut:]




def read_mt_csv(path, symbol, timeframe=1440, **kwargs):

    slice_from = kwargs.get('slice_from', 0)
    slice_to = kwargs.get('slice_to', 0)

    if slice_from == 0 and slice_to == 0:
        cut = kwargs.get('cut', 0)

    if path[-1] != '/':
        path += '/'
    path += symbol + str(timeframe) + '.csv'

    with open(path, 'r') as f:
        csv = f.read()

    lines = [l for l in csv.split('\n')][:-1]
    data = []
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
    elif cut == 0:
        return data
    else:
        return data[-cut:]


# def watcher(fname):
#     d = read_multi_csv(fname)

#     while True:
#         sleep(5)
#         n = read_multi_csv(fname)
#         for k in d.keys():
#             if d[k][-1] != n[k][-1]:
#                 print (k, "HAS CHANGED!")
#             else:
#                 print('...')
#         d = n
