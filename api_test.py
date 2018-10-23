from keys import AV_API_KEY
import json, requests

url='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&outputsize=compact&apikey='+AV_API_KEY


def ask(url):
    method = 'GET'
    response = requests.request(method,url)
    print(response.status_code)
    if response.status_code == requests.codes.ok:
        print (response.text)

ask(url)