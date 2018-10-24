from assets import Asset
from indi import CCI


STOCKS = ['DIS', 'WFC', 'VZ', 'T', 'KO', 'BA', 'ADBE', 'CAT', 'INTC', 'AAPL', 'AXP', 'C', 'CSCO', 'DIS', 'EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'ITX', 'JNJ', 'FE', 'SCI', 'GTN', 'MSGN', 'USM', 'DISCA', 'OGE', 'AROW', 'EXPO', 'TLP', 'MMT', 'LION', 'ATI', 'MYGN']

#STOCKS = ['T']
black=0
white=0
doji =0
hammer = 0
ss = 0
gapup = 0
gapdown = 0
ssum = 0
bs=0
ccup = 0
ccupc = 0

for s in STOCKS:
    chart = Asset()
    chart.load_av_history('AVHD', s)
    chart.range_from_last(750)



    for i in range(chart.range_from, chart.range_to):
        this = chart.get()
        prev = chart.get(-1)

        ssum+=this.close_price - this.open_price
        
        delta = this.close_price - prev.close_price
        #delta = this.close_price - this.open_price

        if prev.is_bullish():
            white = white+delta
        if prev.is_bearish():
            black+=delta
        if prev.is_doji():
            doji+=delta
        if prev.is_hammer():
            hammer +=delta
        if prev.is_shooting_star():
            ss +=delta
        if prev.is_shooting_star() and prev.is_bearish():
            bs+=delta

        cond = CCI(chart.last(14,-1))<0
        if CCI(chart.last(2,-1))>CCI(chart.last(2,-2)) and CCI(chart.last(2,-2))<CCI(chart.last(2,-3)) and cond:
            ccup+=delta
            ccupc +=1
            print (ccup)


        chart.next()

print("B: %r, W: %r, D:%r, H:%r, S:%r, CCUP:%r" % (black, white, doji, hammer, ss, ccup))
print(ccupc)
