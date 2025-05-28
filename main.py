import json
import queue
import socket
import sys
import threading

from client import turn, market_has_camels
from constants import *
from ui import load_images, draw_text, draw_board, select_card
import pygame


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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
images_dict = load_images()
pygame.display.set_caption("Jaipur - Cliente")
clock = pygame.time.Clock()
running = True
selected_cards = []
selected_hand_indices = []
selected_hand_types = []
hand_card_rects = []
card_rects = None
button_rects = []
market_rects = []
selected_cards_market = []
selected_indices_market = []
selected_market_types = []
state = "NOTHING_SELECTED"
current_error_message = ""
hand_length = 0
herd_length = 0

for i in range(7):
    hand_card_rects.append(pygame.rect.Rect(BOTTOM_HAND_X + (PADDING + CARD_WIDTH) * i, BOTTOM_HAND_Y, CARD_WIDTH, CARD_HEIGHT))

for i in range(4):
    button_rects.append(pygame.rect.Rect(BUTTON_X + (BUTTON_WIDTH + PADDING) * i, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
button_rects.append(pygame.rect.Rect(BUTTON_X + (BUTTON_WIDTH + PADDING) * 4, BUTTON_Y, BUTTON_OK_WIDTH, BUTTON_OK_HEIGHT))

for i in range(5):
    market_rects.append(pygame.rect.Rect(MARKET_X + (PADDING + CARD_WIDTH) * i, MARKET_Y, CARD_WIDTH, CARD_HEIGHT))

while running:
    clock.tick(FPS)
    try:
        game_board = game_state_queue.get_nowait()
        herd_length = len(game_board[bottom_player]["herd"])
        hand_length = len(game_board[bottom_player]["hand"])
        card_rects = hand_card_rects[:hand_length]
    except queue.Empty:
        pass

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print("Click en:", mouse_pos)
            if game_board["current_player"] == bottom_player:
                for i, card in enumerate(card_rects):
                    if card.collidepoint(mouse_pos):
                        if card not in selected_cards:
                            selected_cards.append(card)
                            selected_hand_indices.append(i)
                            selected_hand_types.append(game_board[bottom_player]["hand"][i])
                        else:
                            selected_cards.remove(card)
                            selected_hand_indices.remove(i)
                            selected_hand_types.remove(game_board[bottom_player]["hand"][i])
                for i, card in enumerate(market_rects):
                    if card.collidepoint(mouse_pos):
                        if card not in selected_cards_market:
                            selected_cards_market.append(card)
                            selected_indices_market.append(i)
                            selected_market_types.append(game_board["market"][i])
                        else:
                            selected_cards_market.remove(card)
                            selected_indices_market.remove(i)
                            selected_market_types.remove(game_board["market"][i])

                if button_rects[0].collidepoint(mouse_pos):
                    state = "SELL"
                    current_error_message = ""
                if button_rects[1].collidepoint(mouse_pos):
                    state = "EXCHANGE"
                    current_error_message = ""
                if button_rects[2].collidepoint(mouse_pos):
                    state = "TAKE_ONE"
                    current_error_message = ""
                if button_rects[3].collidepoint(mouse_pos):
                    state = "TAKE_CAMELS"
                    current_error_message = ""
                if state in ("SELL", "EXCHANGE", "TAKE_ONE", "TAKE_CAMELS") and button_rects[4].collidepoint(mouse_pos):
                    turn_list = turn(state, selected_hand_indices, selected_hand_types, selected_indices_market, selected_market_types, market_has_camels(game_board["market"]), hand_length, herd_length)

                    if turn_list[0] == 5:
                        current_error_message = turn_list[1]
                    else:
                        client.sendall(json.dumps(turn_list).encode())
                        print("emtro mal")
                    print(selected_hand_indices, selected_hand_types)
                    selected_hand_indices = []
                    selected_hand_types = []
                    selected_cards = []
                    selected_cards_market = []
                    selected_indices_market = []
                    selected_market_types = []
                    state = "NOTHING_SELECTED"

    # Draw
    screen.fill(DARK_GRAY)
    draw_board(screen, game_board, images_dict, top_player, bottom_player, state)
    for card in card_rects:
        if card in selected_cards:
            select_card(screen, YELLOW, card, WIDTH_BORDER)
    for card in market_rects:
        if card in selected_cards_market:
            select_card(screen, YELLOW, card, WIDTH_BORDER)

    if state == "SELL":
        pygame.draw.rect(screen, YELLOW, button_rects[0], WIDTH_BORDER)
    if state == "EXCHANGE":
        pygame.draw.rect(screen, YELLOW, button_rects[1], WIDTH_BORDER)
    if state == "TAKE_ONE":
        pygame.draw.rect(screen, YELLOW, button_rects[2], WIDTH_BORDER)
    if state == "TAKE_CAMELS":
        pygame.draw.rect(screen, YELLOW, button_rects[3], WIDTH_BORDER)
    draw_text(screen,str(current_error_message), MEDIUM_TEXT_SIZE, WIDTH//2 , BUTTON_Y - 35, color=RED, centered=True)

    pygame.display.flip()

pygame.quit()
sys.exit()