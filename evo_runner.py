# LAUNCHER FOR EVO ALGORITHM

from evo import generate
from reader import load_settings_from_report


initial_params = load_settings_from_report('_no_loses.txt')

CHANNEL = ['DIS', 'WFC', 'VZ', 'T', 'KO']
TRENDY = ['BA', 'ADBE', 'CAT', 'INTC', 'AAPL']
OTHER1 = ['AA', 'AXP', 'C', 'CSCO', 'DIS']
OTHER2 = ['EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'ITX', 'JNJ']
FOREX = ['USDJPY']
symbols = []
symbols.extend(TRENDY)
symbols.extend(CHANNEL)
symbols.extend(OTHER1)
symbols.extend(OTHER2)
#symbols.extend(['USDJPY'])

GENERATIONS_COUNT = 20
MUTATIONS = 70
OUTSIDERS = 5
DEPTH = 10
STRATEGY = 'MIN_TRADES_MAX_PROFIT'
#STRATEGY = 'PROFIT_AND_WINRATE'

generate(symbols, 1440, GENERATIONS_COUNT, MUTATIONS, OUTSIDERS, DEPTH, STRATEGY, initial_params=initial_params, cut=250, report=True)
