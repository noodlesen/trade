import dde_client as ddec
import time


# Connect to MT4
# Must register BID and ASK as topics separately..
QUOTE_client = ddec.DDEClient('MT4', 'QUOTE')

# Register desired symbols..
symbols = ['DIS', 'WFC', 'VZ','T', 'KO', 'BA','ADBE', 'CAT', 'INTC', 'AAPL']
for i in symbols:
    QUOTE_client.advise(i)

# Prove it worked:
columns = ['Symbol', 'DATE', 'TIME', 'BID', 'ASK']


while 1:
    time.sleep(1)
    to_display = []
    for item in symbols:
        current_quote = QUOTE_client.request(item).split()
        print(item)
        print ([bytes.decode(c) for c in current_quote])
        print()
