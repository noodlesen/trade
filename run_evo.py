# LAUNCHER FOR EVO ALGORITHM

from evo import generate
from reader import load_settings_from_report
from config import TS


#initial_params = load_settings_from_report('results/TRENDY109.txt')
initial_params = TS.get_random_ts_params()

CHANNEL = ['DIS', 'WFC', 'VZ', 'T', 'KO']
TRENDY = ['BA', 'ADBE', 'CAT', 'INTC', 'AAPL']
OTHER1 = ['AXP', 'C', 'CSCO', 'DIS']
OTHER2 = ['EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'ITX', 'JNJ']
NEW = ['FE', 'SCI', 'GTN', 'MSGN', 'USM', 'DISCA', 'OGE', 'AROW', 'EXPO', 'TLP', 'MMT', 'LION', 'ATI', 'MYGN']

symbols = []
symbols.extend(TRENDY)
#symbols.extend(CHANNEL)
# symbols.extend(OTHER1)
# symbols.extend(OTHER2)
# symbols.extend(NEW)

GENERATIONS_COUNT = 20
MUTATIONS = 70
OUTSIDERS = 5
DEPTH = 10
STRATEGY = 'MAX_ROI_MAX_DIV'


generate(symbols, 1440, GENERATIONS_COUNT, MUTATIONS, OUTSIDERS, DEPTH, STRATEGY, initial_params=initial_params, cut=250, report=True)
