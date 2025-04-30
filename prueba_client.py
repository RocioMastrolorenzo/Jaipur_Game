from client import get_take_one_resource_input

aaaaa = {
    'deck': ['si', 'cl', 'sp', 'di', 'si', 'cl', 'cl', 'le', 'sp', 'si', 'le', 'cl', 'cl', 'ca', 'ca', 'di', 'go', 'le',
             'go', 'ca', 'go', 'si', 'si', 'sp', 'le', 'di', 'ca', 'le', 'sp', 'go', 'go', 'ca', 'le', 'ca', 'sp', 'ca',
             'cl', 'si', 'di', 'le'],
    'market': ['ca', 'ca', 'ca', 'sp', 'di'],
    'tokens': {'di': [7, 7, 5, 5, 5], 'go': [6, 6, 5, 5, 5], 'si': [5, 5, 5, 5, 5], 'cl': [5, 3, 3, 2, 2, 1, 1],
               'sp': [5, 3, 3, 2, 2, 1, 1], 'le': [4, 3, 2, 1, 1, 1, 1, 1, 1], 'x5': [8, 9, 10, 8, 10],
               'x4': [4, 4, 5, 5, 6, 6], 'x3': [3, 3, 1, 1, 2, 2, 2], 'ca': [5]},
    'player1': {'hand': ['di', 'go', 'cl', 'sp', 'sp'], 'herd': [], 'token_pile': [], 'token_tally': 0},
    'player2': {'hand': ['le', 'le', 'le', 'cl'], 'herd': ['ca'], 'token_pile': [], 'token_tally': 0}}

get_take_one_resource_input(aaaaa)