import socket

from board import Board
from deck import Deck
from jaipur import turn
from player import Player


def send_board(p1,p2, board):
    p1.conn.sendall(board.jsonify().encode())
    p2.conn.sendall(board.jsonify().encode())

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
    player1_name = "a"
    player2_name = "b"
    player1 = Player(player1_name)
    player1.conn = player_connections[0]
    player2 = Player(player2_name)
    player2.conn = player_connections[1]
    deck.shuffle_cards()
    player1.deal_hand(deck)
    player2.deal_hand(deck)
    board = Board(player1, player2, deck)

    # Gameplay

    while not board.round_end_check():
        board.current_player.sort_hand()
        print(board)
        send_board(player1, player2, board)
        print(f"{board.current_player.name}'s turn: \n")
        turn(board.current_player)
        board.fill_market()
        board.switch_players()
    board.give_camel_token()
    board.give_point()
