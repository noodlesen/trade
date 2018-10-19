from time import sleep
rys =[]
tys = []
tds = []
while True:
    with open("C:\\Program Files (x86)\\ForexClub MT4\\MQL4\\Files\\fxexp.txt", 'r') as f:
        file_data = (f.read())

        prices = {}
        lines = file_data.split('\n')
        for l in lines:
            tokens = l.split(';')
            if tokens[0] == 'MARKET':
                prices[tokens[1]] = {"BID": float(tokens[2]), "ASK": float(tokens[3]), "TIMESTAMP": int(tokens[4])}

        ry = prices['USDJPY']['ASK']
        ty = round(prices['USDJPY']['ASK']+prices['EURJPY']['ASK']+prices['CHFJPY']['ASK']+prices['GBPJPY']['ASK']+1, 3)
        td = round(prices['EURUSD']['ASK']+prices['GBPUSD']['ASK']+1/prices['USDCHF']['ASK']+1/prices['USDJPY']['ASK']+1, 5)

        rys.append(ry)
        tys.append(ty)
        tds.append(td)

        dl = len(rys)
        if dl<50:
            x = dl
        else:
            x = 50

        rya = sum(rys[-x:])/x
        tya = sum(tys[-x:])/x
        tda = sum(tds[-x:])/x


        print()
        print (ry, ty, td)
        print(round(rya,3), round(tya,3), round(tda,6))
        print(round(ry-rya,3), round(ty-tya,3), round((td-tda)/tda,6))

    sleep(5)


