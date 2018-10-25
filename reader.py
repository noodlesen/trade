# DATA READING LIBRARY

import json
from keys import AV_API_KEY
import requests
from time import sleep

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


def ask_av_history(stocks):
    SLEEP = 10
    for symbol in stocks:
        print ('requesting '+symbol)
        url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=' % symbol
        response = requests.request('GET',url+AV_API_KEY)
        print(response.status_code)
        if response.status_code == requests.codes.ok:
            print ('OK')
            with open('AVHD/'+symbol+'.json', 'w') as f:
                f.write(response.text)
            for n in range(SLEEP):
                sleep(1)
                print('.')
            print()


def ask_av_indi(s,i):
    url="https://www.alphavantage.co/query?function=%s&symbol=%s&interval=daily&time_period=10&apikey=" % (i,s)
    response = requests.request('GET',url+AV_API_KEY)
    print(response.status_code)
    if response.status_code == requests.codes.ok:
        print ('OK')
        with open('INDI/'+s+i+'.json', 'w') as f:
            f.write(response.text)






