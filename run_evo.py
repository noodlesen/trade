# LAUNCHER FOR EVO ALGORITHM

from evo import generate
from reader import load_settings_from_report


initial_params = load_settings_from_report('results/R33SL.txt')

CHANNEL = ['DIS', 'WFC', 'VZ', 'T', 'KO']
TRENDY = ['BA', 'ADBE', 'CAT', 'INTC', 'AAPL']
OTHER1 = ['AXP', 'C', 'CSCO', 'DIS']
OTHER2 = ['EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'ITX', 'JNJ']
NEW = ['FE', 'SCI', 'GTN', 'MSGN', 'USM', 'DISCA', 'OGE', 'AROW', 'EXPO', 'TLP', 'MMT', 'LION', 'ATI', 'MYGN']

symbols = []
symbols.extend(TRENDY)
symbols.extend(CHANNEL)
symbols.extend(OTHER1)
symbols.extend(OTHER2)
symbols.extend(NEW)

GENERATIONS_COUNT = 1
MUTATIONS = 70
OUTSIDERS = 5
DEPTH = 10
STRATEGY = 'MAX_ROI'
#STRATEGY = 'MAX_ROI_MIN_LOSS'
#STRATEGY = 'MIN_TRADES_MAX_PROFIT'
#STRATEGY = 'PROFIT_AND_WINRATE'

generate(symbols, 1440, GENERATIONS_COUNT, MUTATIONS, OUTSIDERS, DEPTH, STRATEGY, initial_params=initial_params, cut=750, report=True)
