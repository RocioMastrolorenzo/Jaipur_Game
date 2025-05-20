import socket
import json

class GoBack(Exception):
    pass

def turn(player, board):
    while True:
        try:
            chosen_turn = choose_turn()
            if chosen_turn == 1:  # sell
                user_type, user_amount = get_sell_input(player, board)
                return [chosen_turn, user_type, user_amount]
            elif chosen_turn == 2:  # exchange
                player_indices, market_indices = get_exchange_input(player, board)
                return [chosen_turn, player_indices, market_indices]
            elif chosen_turn == 3:  # take one
                card_index = get_take_one_resource_input(player, board)
                return [chosen_turn, card_index]
            elif chosen_turn == 4:  # take all camels
                get_take_all_camels_input(board)
                return [chosen_turn]
        except GoBack as e:
            print(e)


def check_goback(string:str):
    if "back" in string.lower():
        raise GoBack


def get_sell_input(player, board):
    user_amount = ""
    user_type = ""
    valid_inputs = {
        "diamond": "di",
        "diamonds": "di",
        "di": "di",
        "gold": "go",
        "go": "go",
        "silver": "si",
        "si": "si",
        "cloth": "cl",
        "cl": "cl",
        "spices": "sp",
        "spice": "sp",
        "sp": "sp",
        "leather": "le",
        "le": "le",
        "camel": "ca",
        "camels": "ca",
        "ca": "ca",
    }
    expensive_resources = ["di", "go", "si"]
    print(board[player]["hand"])
    while True:
        try:
            user_amount = input("Enter amount to sell ")
            check_goback(user_amount)
            user_amount = int(user_amount)
            if user_amount > len(board[player]["hand"]):
                raise ValueError("You can't sell more cards than the amount you have in your hand")
            elif user_amount <= 0:
                raise ValueError("You can't sell less than one card")

            user_type_input = input("Enter type of resource to sell ")
            check_goback(user_type_input)
            if user_type_input in valid_inputs:
                user_type = valid_inputs[user_type_input]
            if user_type_input not in valid_inputs:
                raise ValueError("Enter a valid type of resource")
            if user_type == "ca":
                raise ValueError("You can't sell camels")
            if user_type in expensive_resources and user_amount < 2:
                raise ValueError("You need to sell at least two of this type of resource")
            if user_amount > board[player]["hand"].count(user_type):
                raise ValueError("You don't have enough cards of this type")
            break
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print("Enter a valid number")
            else:
                print(e)
            continue

    return user_type, user_amount


def get_exchange_input(player, board):
    market_indices = ""
    player_indices = ""

    while True:
        try:
            print_market(board)
            market_indices = input("choose the cards you want to exchange separated by spaces: ")
            check_goback(market_indices)
            market_indices = list({int(i) for i in market_indices.split(" ")}) # is a set first to remove duplicates

            if len(market_indices) < 2:
                raise ValueError("You must exchange at least two cards")
            if len(board["market"]) < len(market_indices):
                raise ValueError("There's not enough cards in the market")

            market_types = set()
            for i in market_indices:
                if i >= len(board["market"]):
                    raise ValueError(f"{i} is not a valid card number.")
                if board["market"][i] == "ca":
                    raise ValueError("You can't exchange camels")
                market_types.add(board["market"][i])

            market_indices.sort()

            print_hand(player, board)
            player_indices = input(f"select {len(market_indices)} of your cards separated by spaces: ")
            check_goback(player_indices)
            player_indices = list({int(i) for i in player_indices.split(" ")})
            player_indices.sort()

            if len(board[player]["hand"]) + len(board[player]["herd"]) < len(player_indices):
                raise ValueError("You don't have enough cards in your hand")

            player_types = set()
            for i in player_indices:
                if i >= len(board[player]["hand"]) + len(board[player]["herd"]):
                    raise ValueError(f"{i} is not a valid card number.")
                if i >= len(board[player]["hand"]):
                    player_types.add(board[player]["herd"][0])
                else:
                    player_types.add(board[player]["hand"][i])

            if len(market_indices) != len(player_indices):
                raise ValueError("You must exchange the same amount of cards")

            if player_types.intersection(market_types):
                raise ValueError("You can't exchange the same type of card")

            # Calculates the amount of chosen cards that are camels, to see if the resulting hand will be over hand size limit
            chosen_camels = len([i for i in player_indices if i > len(board[player]["hand"]) - 1])
            if len(board[player]["hand"]) + chosen_camels > 7:
                raise ValueError("You can't have more than seven cards in your hand")

            break
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print("Enter valid numbers separated by spaces")
            else:
                print(e)
            continue

    for i in range(len(player_indices)):
        if player_indices[i] >= len(board[player]["hand"]):
            player_indices[i] = 99

    return player_indices, market_indices


def get_take_one_resource_input(player, board):
    card_index_user = ""
    if len(board[player]["hand"]) >= 7:
        raise GoBack("You can't have more than seven cards in your hand")
    while True:
        try:
            print_market(board)
            card_index_user = input("Select the card to take ")
            check_goback(card_index_user)
            card_index_user = int(card_index_user)
            if card_index_user >= len(board["market"]):
                raise ValueError(f"{card_index_user} is not a valid card number.")
            if board["market"][card_index_user] == "ca":
                raise ValueError("You can't take a single camel")
            break
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                print("Enter a valid number")
            else:
                print(e)
            continue

    return card_index_user

def get_take_all_camels_input(board):
    if "ca" not in board["market"]:
        raise GoBack("There's no camels to take")


def print_hand(player, board):
    string_hand = ""

    # adds the cards from the hand
    string_hand += f"{board[player]["hand"]}| "

    # adds the cards from the herd
    string_hand += f"{board[player]["herd"]}\n"

    # adds the index number on the bottom
    for i in range(len(board[player]["hand"])):
        string_hand += "  " + str(i) + "   "

    string_hand += "| "

    for i in range(len(board[player]["herd"])):
        string_hand += "  " + str(i + len(board[player]["hand"])) + "  "

    print(string_hand)


def print_market(board):
    str_market = ""

    # adds the cards from the market
    str_market += f"{board["market"]}\n"

    # adds the index number on the bottom
    for i in range(len(board["market"])):
        str_market += "  " + str(i) + "   "

    print(str_market)


def choose_turn():
    # dictionary of valid words to input in addition to the corresponding number
    valid_inputs = {
        "1": 1, "sell": 1, "sell cards": 1,
        "2": 2, "exchange": 2, "exchange cards": 2,
        "3": 3, "take": 3, "take one": 3, "resource": 3, "take one resource": 3,
        "4": 4, "camels": 4, "take camels": 4, "take all camels": 4, "camel": 4
    }
    while True:
        print()
        user_turn_input = input("Choose your action to play \n"
                                "1. Sell cards\n"
                                "2. Exchange cards\n"
                                "3. Take one resource\n"
                                "4. Take all camels\n"
                                ).strip().lower()

        if user_turn_input in valid_inputs:
            return valid_inputs[user_turn_input]  # returns an int
        else:
            print("Enter a valid action")

def print_board(board, top_player, bottom_player):
    s = ""
    blank_line = " " * 104 + "\n"

    s += "+" + "-" * 104 + "+" + "\n"
    s += f'{" " * 10}Opponent hand:  {'[??] ' * len(board[top_player]["hand"])}\n'
    s += blank_line
    s += f'{'Opponent herd: ' + str(len(board[top_player]["herd"])) :^104}\n'
    s += f'{'Deck: ' + str(len(board["deck"])):^104}\n'
    s += f'{"Tokens: " + str(board[top_player]["token_bonus_amount"]):>104}\n'
    s += f'{"Current points: " + str(game_board_incoming[top_player]["token_tally"]):>104}\n'
    s += blank_line
    for resource in board["tokens"]:
        s += str(resource) + " | "
        for value in board["tokens"][resource]:
            s += str(value) + " "
        s += '\n'
    s += f'{" " * 30}{board["market"]}\n'
    s += blank_line
    s += f'{"Tokens: " + str(board[bottom_player]["token_bonus_amount"]):>104}\n'
    s += f'{"Current points: " + str(board[bottom_player]["token_tally"]):>104}\n'
    s += f'{'Your herd: ' + str(len(board[bottom_player]["herd"])) :^104}\n'
    s += blank_line
    s += f'{" " * 10} Your hand: {board[bottom_player]["hand"]}\n'
    s += "+" + "-" * 104 + "+" + "\n"
    return print(s)

def play_again():
    while True:
        try:
            play_again = input("Play again? Yes/No ").upper()
            if play_again == "YES" or play_again == "Y":
                return False
            elif play_again == "NO" or play_again == "N":
                return True
            else:
                raise ValueError
        except ValueError:
            print("Enter a valid response. (Yes or No)")


if __name__ == '__main__':
    HOST = '127.0.0.1'
    HOST = input("Enter IP")
    PORT = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    welcome = client.recv(4096).decode()
    print(welcome)

    if "Player 1" in welcome:
        bottom_player = "player1"
        top_player = "player2"
    else:
        top_player = "player1"
        bottom_player = "player2"

    round_end = False
    game_end = False
    stop_playing = False

    while not stop_playing:
        while not game_end:
            while not round_end:
                print("llego")
                msg = client.recv(4096).decode()
                print(msg)
                game_board_incoming = json.loads(msg)

                """
                print(game_board_incoming)
        
                temp = {
                    'deck': ['si', 'cl', 'sp', 'di', 'si', 'cl', 'cl', 'le', 'sp', 'si', 'le', 'cl', 'cl', 'ca', 'ca', 'di', 'go', 'le',
                             'go', 'ca', 'go', 'si', 'si', 'sp', 'le', 'di', 'ca', 'le', 'sp', 'go', 'go', 'ca', 'le', 'ca', 'sp', 'ca',
                             'cl', 'si', 'di', 'le'],
                    'market': ['ca', 'ca', 'ca', 'sp', 'di'],
                    'tokens': {'di': [7, 7, 5, 5, 5], 'go': [6, 6, 5, 5, 5], 'si': [5, 5, 5, 5, 5], 'cl': [5, 3, 3, 2, 2, 1, 1],
                               'sp': [5, 3, 3, 2, 2, 1, 1], 'le': [4, 3, 2, 1, 1, 1, 1, 1, 1], 'x5': [8, 9, 10, 8, 10],
                               'x4': [4, 4, 5, 5, 6, 6], 'x3': [3, 3, 1, 1, 2, 2, 2], 'ca': [5]},
                    'current_player': "player1" ,
                    'player1': {'hand': ['di', 'go', 'cl', 'sp', 'sp'], 'herd': [], 'token_pile': [], 'token_tally': 0},
                    'player2': {'hand': ['le', 'le', 'le', 'cl'], 'herd': ['ca'], 'token_pile': [], 'token_tally': 0}}
                """
                print_board(game_board_incoming, top_player, bottom_player)

                turn_msg = f"{game_board_incoming["current_player"]}'s turn: \n"
                print(turn_msg)

                if bottom_player in turn_msg:
                    client.sendall(json.dumps(turn(bottom_player, game_board_incoming)).encode())
                elif top_player in turn_msg:
                    print("waiting for opponent...")

                round_end = bool(int(client.recv(1).decode()))
                print(round_end)
            round_end = False
            round_winner = client.recv(7).decode()
            print(round_winner)
            game_end = bool(int(client.recv(1).decode()))
            print(game_end)
        game_end = False
        client.sendall(str(int(play_again())).encode())
        stop_playing = bool(int(client.recv(1).decode()))