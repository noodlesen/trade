from keys import AV_API_KEY
import json, requests
from time import sleep

API_URL='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey='+AV_API_KEY

BASE_STOCKS = ['DIS', 'WFC', 'VZ', 'T', 'KO', 'BA', 'ADBE', 'CAT', 'INTC', 'AAPL', 'AA', 'AXP', 'C', 'CSCO', 'DIS', 'EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'ITX', 'JNJ']

def ask(symbol):
    print ('requesting '+symbol)
    method = 'GET'
    url = API_URL % symbol
    response = requests.request(method,url)
    print(response.status_code)
    if response.status_code == requests.codes.ok:
        print ('OK')
        print()
        with open('AVHD/'+symbol+'.json', 'w') as f:
            f.write(response.text)
        sleep(10)


# for s in BASE_STOCKS:
#     ask(s)

ask('SPY')