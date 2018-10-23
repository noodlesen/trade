# LAUNCHER FOR EVO ALGORITHM

from evo import generate
from reader import load_settings_from_report


initial_params = load_settings_from_report('roi87.txt')

CHANNEL = ['DIS', 'WFC', 'VZ', 'T', 'KO']
TRENDY = ['BA', 'ADBE', 'CAT', 'INTC', 'AAPL']
OTHER1 = ['AXP', 'C', 'CSCO', 'DIS']
OTHER2 = ['EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'ITX', 'JNJ']

symbols = []
symbols.extend(TRENDY)
symbols.extend(CHANNEL)
symbols.extend(OTHER1)
symbols.extend(OTHER2)

GENERATIONS_COUNT = 10
MUTATIONS = 70
OUTSIDERS = 5
DEPTH = 10
STRATEGY = 'MAX_ROI'
#STRATEGY = 'MIN_TRADES_MAX_PROFIT'
#STRATEGY = 'PROFIT_AND_WINRATE'

generate(symbols, 1440, GENERATIONS_COUNT, MUTATIONS, OUTSIDERS, DEPTH, STRATEGY, initial_params=initial_params, cut=500, report=True)
