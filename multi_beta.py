from assets import MultiAsset

m = MultiAsset()
TRENDY = ['BA', 'ADBE', 'CAT', 'INTC', 'AAPL']
for t in TRENDY:
    m.load_mt4_history('MTDATA',t, 1440)
m.show()
m.reset()