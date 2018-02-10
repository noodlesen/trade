from holder import Asset


def typical_price(bar):
    return (bar['high']+bar['low']+bar['close'])/3

def CCI(data):

    n = len(data)
    tp_price_list = [typical_price(d) for d in data]
    tp_avg = sum(tp_price_list)/n
    md = sum([abs(tp_avg-tp) for tp in tp_price_list])/3
    md = 0.0000001 if md == 0 else md
    return round((typical_price(data[-1])-tp_avg)/(0.015*md),2)

# a = Asset()
# a.load_mt4_history('MTDATA', 'ADBE', 1440)
# ofs = 7
# for i in range (0+ofs,len(a.data)):
#     print (CCI(a.data[i-2:i]), a.data[i]['date'], a.data[i]['time'])
