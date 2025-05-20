import json
import queue
import socket
import sys
import threading

from client import turn
from constants import *
from ui import load_images, draw_text, draw_board
import pygame


def turn_taker(board_queue, bottom_player, conn):
    while True:
        board = board_queue.get()
        print(board["current_player"])
        if board["current_player"] == bottom_player:
            conn.sendall(json.dumps(turn(board["current_player"], board)).encode())

def socket_receive_messages(conn, game_state_queue, board_queue):
    while True:
        msg = conn.recv(4096).decode()
        dic = json.loads(msg)
        game_state_queue.put(dic)
        board_queue.put(dic)

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

game_state_queue = queue.Queue()
board_queue = queue.Queue()

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

game_start = client.recv(4096).decode()
game_board = {'deck': [],
        'market': [],
        'tokens': {'di': [5, 5, 5, 7, 7], 'go': [5, 5, 5, 6, 6], 'si': [5, 5, 5, 5, 5], 'cl': [1, 1, 2, 2, 3, 3, 5],
                   'sp': [1, 1, 2, 2, 3, 3, 5], 'le': [1, 1, 1, 1, 1, 1, 2, 3, 4], 'x5': [8, 9, 10, 8, 10],
                   'x4': [4, 4, 5, 5, 6, 6], 'x3': [3, 3, 1, 1, 2, 2, 2], 'ca': [5]},
        'current_player': "",
        'player1': {'hand': [], 'herd': [], 'token_bonus_amount': {'x3': 0, 'x4': 0, 'x5': 0}, 'token_tally': 0},
        'player2': {'hand': [], 'herd': [], 'token_bonus_amount': {'x3': 0, 'x4': 0, 'x5': 0}, 'token_tally': 0,}}
board_queue.put(game_board)

threading.Thread(target=socket_receive_messages,args=(client,game_state_queue, board_queue), daemon=True).start()
threading.Thread(target=turn_taker, args=(board_queue, bottom_player, client), daemon=True).start()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
images_dict = load_images()
pygame.display.set_caption("Jaipur - Cliente")
clock = pygame.time.Clock()

running = True

while running:
    clock.tick(FPS)
    try:
        game_board = game_state_queue.get_nowait()
    except queue.Empty:
        pass

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print("Click en:", mouse_pos)
            # Acá podrías detectar clicks sobre cartas o botones

    # Dibujar
    screen.fill(DARK_GRAY)
    draw_board(screen, game_board, images_dict, top_player, bottom_player)

    pygame.display.flip()

pygame.quit()
sys.exit()