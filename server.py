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
    if input[0] == 1:
        player.sell(board, input[1], input[2])
    elif input[0] == 2:
        player.exchange(board, input[1], input[2])
    elif input[0] == 3:
        player.take_one_resource(board, input[1])
    elif input[0] == 4:
        player.take_all_camels(board)

def send_round_status():
    if round_end:
        player1.conn.sendall("1".encode())
        player2.conn.sendall("1".encode())
    else:
        player1.conn.sendall("0".encode())
        player2.conn.sendall("0".encode())
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
    deck = Deck()
    # player1_name = input("Enter the name of the first player: ")
    # player2_name = input("Enter the name of the second player: ")
    player1_name = "player1"
    player2_name = "player2"
    player1 = Player(player1_name)
    player1.conn = player_connections[0]
    player2 = Player(player2_name)
    player2.conn = player_connections[1]
    deck.shuffle_cards()
    player1.deal_hand(deck)
    player2.deal_hand(deck)
    board = Board(player1, player2, deck)
    round_end = board.round_end_check()

    # Gameplay

    while not round_end:
        board.current_player.sort_hand()
        send_board(player1, player2, board)
        turn_msg = f"{board.current_player.name}'s turn: \n".encode()
        player1.conn.sendall(turn_msg)
        player2.conn.sendall(turn_msg)
        turn_input = board.current_player.conn.recv(4096).decode()
        turn_input = json.loads(turn_input )
        print(turn_input)
        play_turn(turn_input, board.current_player, board)
        print(board)
        print(board.market)
        board.fill_market()
        print("llenó market")
        print(board.market)
        print(board.current_player)
        board.switch_players()
        print(board.current_player)
        print("switcheó players")
        round_end = board.round_end_check()
        print(f"Terminó? {round_end}")
        send_round_status()
        print("Mandó status")
    board.give_camel_token()
    board.give_point()
