import pprint
import socket
import json
from os.path import split

from board import Board
from deck import Deck
from jaipur import turn
from player import Player
from pprint import pp

def send_board(p1,p2, board):
    pprint.pp(board.jsonify())
    p1.conn.sendall(board.jsonify().encode())
    p2.conn.sendall(board.jsonify().encode())

def play_turn(input, player, board):
    """
    Chooses the selected turns and plays it.

    :param input: <List[int]> the first index is the selected turn, then the other numbers are the info required for each
    specific turn
    :param player: <Player> The current player
    :param board: <Board> Board object
    :return: None
    """
    if input[0] == 1:
        player.sell(board, input[1], input[2])
    elif input[0] == 2:
        player.exchange(board, input[1], input[2])
    elif input[0] == 3:
        player.take_one_resource(board, input[1])
    elif input[0] == 4:
        player.take_all_camels(board)

def send_str_to_both(p1,p2,s):
    msg = s.encode()
    p1.conn.sendall(msg)
    p2.conn.sendall(msg)

def stop_playing_check(stop_playing_p1, stop_playing_p2):
    return bool(int(stop_playing_p1)) or bool(int(stop_playing_p2))

if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)

    print("Server waiting for players...")

    player_connections = []
    addresses = []

    # Accept two players
    for i in range(2):
        conn, addr = server.accept()
        print(f"Player {i + 1} connected from {addr}")
        conn.sendall(f"You are Player {i + 1}".encode())
        player_connections.append(conn)
        addresses.append(addr)

    # initial setup

    # player1_name = input("Enter the name of the first player: ")
    # player2_name = input("Enter the name of the second player: ")
    player1_name = "player1"
    player2_name = "player2"
    player1 = Player(player1_name)
    player1.conn = player_connections[0]
    player2 = Player(player2_name)
    player2.conn = player_connections[1]
    game_end = False
    round_end = False
    stop_playing = False
    # Gameplay
    while True:
        while not stop_playing:

            while not game_end:
                print("1")
                player1.empty_player()
                player2.empty_player()
                print("2")
                deck = Deck(debug=True)
                deck.shuffle_cards()
                board = Board(player1, player2, deck)
                print("3")
                player1.deal_hand(deck)
                player2.deal_hand(deck)
                print("4")
                while not round_end:
                    print("5")
                    board.current_player.sort_hand()
                    print("llego???")
                    send_board(player1, player2, board)
                    turn_input = board.current_player.conn.recv(4096).decode()
                    turn_input = json.loads(turn_input)
                    print(turn_input)
                    play_turn(turn_input, board.current_player, board)
                    player1.count_tokens_no_bonus()
                    player2.count_tokens_no_bonus()
                    print(board)
                    print(board.market)
                    round_end = board.round_end_check()
                    print(f"Terminó? {round_end}")
                    if not round_end:
                        board.fill_market()
                        print("llenó market")
                    print(board.market)
                    print(board.current_player)
                    board.switch_players()
                    print(board.current_player)
                    print("switcheó players")
                    send_str_to_both(player1, player2, str(int(round_end)))
                    print("Mandó status")
                board.give_camel_token()
                print(board.tokens)
                round_winner = board.give_point()
                send_str_to_both(player1, player2, round_winner)
                print(f"Player 1: {player1.count_points()} Player 2: {player2.count_points()} \n{round_winner} wins!")
                print(player1.score)
                print(player2.score)
                game_end = board.game_end_check()
                send_str_to_both(player1, player2, str(int(game_end)))
                round_end = False
            game_end = False
            player1.score = 0
            player2.score = 0
            stop_playing_p1 = player1.conn.recv(1).decode()
            stop_playing_p2 = player2.conn.recv(1).decode()
            stop_playing = stop_playing_check(stop_playing_p1, stop_playing_p2)
            send_str_to_both(player1, player2, str(int(stop_playing)))
input()
