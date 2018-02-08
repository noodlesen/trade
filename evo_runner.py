# LAUNCHER FOR EVO ALGORITHM

from evo import generate
from reader import load_settings_from_report


# initial_params = {
#         "FTP": 0.0565,
#         "cut_mix": 0.14,
#         "cut_period": 16,
#         "cut_treshold": 0.021,
#         "fia_dmax": 9,
#         "fia_dmin": 2,
#         "fia_treshold": 0.1,
#         "init_sl_k": 0.933,
#         "init_tp": 28,
#         "ptdj_mix": 0.52,
#         "pth_mix": 0.87,
#         "ptss_mix": 0.71,
#         "tp_koef": 1.3,
#         "use_BREAK": True,
#         "use_BREAKEVEN": False,
#         "use_CUT": False,
#         "use_FIA": True,
#         "use_FTP": True,
#         "use_GAP": False,
#         "use_PTDJ": False,
#         "use_PTH": False,
#         "use_PTSS": True
# }

initial_params = load_settings_from_report('_jpy_60.txt')#'results_abs_tp/_41K_in_2y_15sym.txt')
# print(initial_params)

CHANNEL = ['DIS', 'WFC', 'VZ','T', 'KO']
TRENDY = ['BA','ADBE', 'CAT', 'INTC', 'AAPL']
OTHER1 = ['AA', 'AXP', 'C', 'CSCO', 'DIS']
OTHER2 = ['EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'ITX', 'JNJ']
FOREX = ['USDJPY']
symbols = []
# symbols.extend(TRENDY)
# symbols.extend(CHANNEL)
# symbols.extend(OTHER1)
# symbols.extend(OTHER2)
symbols.extend(FOREX)



GENERATIONS_COUNT = 300

MUTATIONS = 8
OUTSIDERS = 4
DEPTH = 4
STRATEGY = 'PROFIT_AND_WINRATE'

# GENERATIONS_COUNT = 10
# MUTATIONS = 4
# OUTSIDERS = 0
# DEPTH =7
# STRATEGY = 'MAX_PROFIT'

generate(symbols, 60, GENERATIONS_COUNT, MUTATIONS, OUTSIDERS, DEPTH, STRATEGY, cut=500, report=True) #  initial_params=initial_params


