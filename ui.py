import pygame
import sys

from constants import *

# Configuración de ventana
WIDTH, HEIGHT = 1920, 1080
FPS = 60

# Colores útiles



def load_images():
    mat_image = pygame.image.load("assets/mat.png")
    mat_image = pygame.transform.scale(mat_image, (WIDTH, HEIGHT)).convert()
    card_back = pygame.image.load("assets/card_back.png")
    card_back = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT)).convert()
    card_camel = pygame.image.load("assets/card_camel.png")
    card_camel = pygame.transform.scale(card_camel, (CARD_WIDTH, CARD_HEIGHT)).convert()
    card_diamond = pygame.image.load("assets/card_diamond.png")
    card_diamond = pygame.transform.scale(card_diamond, (CARD_WIDTH, CARD_HEIGHT)).convert()
    card_gold = pygame.image.load("assets/card_gold.png")
    card_gold = pygame.transform.scale(card_gold, (CARD_WIDTH, CARD_HEIGHT)).convert()
    card_silver = pygame.image.load("assets/card_silver.png")
    card_silver = pygame.transform.scale(card_silver, (CARD_WIDTH, CARD_HEIGHT)).convert()
    card_cloth = pygame.image.load("assets/card_cloth.png")
    card_cloth = pygame.transform.scale(card_cloth, (CARD_WIDTH, CARD_HEIGHT)).convert()
    card_spices = pygame.image.load("assets/card_spices.png")
    card_spices = pygame.transform.scale(card_spices, (CARD_WIDTH, CARD_HEIGHT)).convert()
    card_leather = pygame.image.load("assets/card_leather.png")
    card_leather = pygame.transform.scale(card_leather, (CARD_WIDTH, CARD_HEIGHT)).convert()
    card_camel_sideways = pygame.image.load("assets/card_camel.png")
    card_camel_sideways = pygame.transform.scale(card_camel_sideways, (CARD_WIDTH, CARD_HEIGHT)).convert()
    card_camel_sideways = pygame.transform.rotate(card_camel_sideways, 90)
    token_leather_1 = pygame.image.load("assets/leather_1.png")
    token_leather_1 = pygame.transform.scale(token_leather_1, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_leather_2 = pygame.image.load("assets/leather_2.png")
    token_leather_2 = pygame.transform.scale(token_leather_2, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_leather_3 = pygame.image.load("assets/leather_3.png")
    token_leather_3 = pygame.transform.scale(token_leather_3, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_leather_4 = pygame.image.load("assets/leather_4.png")
    token_leather_4 = pygame.transform.scale(token_leather_4, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_cloth_1 = pygame.image.load("assets/cloth_1.png")
    token_cloth_1 = pygame.transform.scale(token_cloth_1, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_cloth_2 = pygame.image.load("assets/cloth_2.png")
    token_cloth_2 = pygame.transform.scale(token_cloth_2, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_cloth_3 = pygame.image.load("assets/cloth_3.png")
    token_cloth_3 = pygame.transform.scale(token_cloth_3, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_cloth_5 = pygame.image.load("assets/cloth_5.png")
    token_cloth_5 = pygame.transform.scale(token_cloth_5, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_spice_1 = pygame.image.load("assets/spice_1.png")
    token_spice_1 = pygame.transform.scale(token_spice_1, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_spice_2 = pygame.image.load("assets/spice_2.png")
    token_spice_2 = pygame.transform.scale(token_spice_2, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_spice_3 = pygame.image.load("assets/spice_3.png")
    token_spice_3 = pygame.transform.scale(token_spice_3, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_spice_5 = pygame.image.load("assets/spice_5.png")
    token_spice_5 = pygame.transform.scale(token_spice_5, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_silver_5 = pygame.image.load("assets/silver_5.png")
    token_silver_5 = pygame.transform.scale(token_silver_5, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_gold_5 = pygame.image.load("assets/gold_5.png")
    token_gold_5 = pygame.transform.scale(token_gold_5, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_gold_6 = pygame.image.load("assets/gold_6.png")
    token_gold_6 = pygame.transform.scale(token_gold_6, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_diamond_5 = pygame.image.load("assets/diamond_5.png")
    token_diamond_5 = pygame.transform.scale(token_diamond_5, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_diamond_7 = pygame.image.load("assets/diamond_7.png")
    token_diamond_7 = pygame.transform.scale(token_diamond_7, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_camel_5 = pygame.image.load("assets/camel_5.png")
    token_camel_5 = pygame.transform.scale(token_camel_5, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_x3 = pygame.image.load("assets/token_x3.png")
    token_x3 = pygame.transform.scale(token_x3, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_x4 = pygame.image.load("assets/token_x4.png")
    token_x4 = pygame.transform.scale(token_x4, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()
    token_x5 = pygame.image.load("assets/token_x5.png")
    token_x5 = pygame.transform.scale(token_x5, (TOKEN_WIDTH, TOKEN_HEIGHT)).convert_alpha()


    images_dict = {
        "mat": mat_image,
        "cards": {
            "camel_sideways": card_camel_sideways,
            "back": card_back,
            "ca": card_camel,
            "di": card_diamond,
            "go": card_gold,
            "si": card_silver,
            "cl": card_cloth,
            "sp": card_spices,
            "le": card_leather,
        },
        "tokens": {
            "le1": token_leather_1,
            "le2": token_leather_2,
            "le3": token_leather_3,
            "le4": token_leather_4,
            "cl1": token_cloth_1,
            "cl2": token_cloth_2,
            "cl3": token_cloth_3,
            "cl5": token_cloth_5,
            "sp1": token_spice_1,
            "sp2": token_spice_2,
            "sp3": token_spice_3,
            "sp5": token_spice_5,
            "si5": token_silver_5,
            "go5": token_gold_5,
            "go6": token_gold_6,
            "di5": token_diamond_5,
            "di7": token_diamond_7,
            "ca": token_camel_5,
            "x3": token_x3,
            "x4": token_x4,
            "x5": token_x5,
        }
    }
    return images_dict

def draw_text(screen, text, size, x, y, color=WHITE, centered=False):
    font = pygame.font.SysFont("roboto", size)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if centered:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)


def draw_board(screen, game_board, images, top_player, bottom_player):
    screen.blit(images["mat"], (0, 0))
    for i, card in enumerate(game_board["market"]):
        screen.blit(images["cards"][card], (MARKET_X + (PADDING + CARD_WIDTH) * i,MARKET_Y))
    for i, card in enumerate(game_board[bottom_player]["hand"]):
        screen.blit(images["cards"][card], (BOTTOM_HAND_X + (PADDING + CARD_WIDTH) * i, BOTTOM_HAND_Y))
    for i, card in enumerate(game_board[top_player]["hand"]):
        screen.blit(images["cards"]["back"], (TOP_HAND_X + (PADDING + CARD_WIDTH) * i, TOP_HAND_Y))
    for i, card in enumerate(game_board[bottom_player]["herd"]):
        screen.blit(images["cards"]["camel_sideways"], (BOTTOM_HERD_X, BOTTOM_HERD_Y - 6 * i))
    for i, card in enumerate(game_board[top_player]["herd"]):
        screen.blit(images["cards"]["camel_sideways"], (TOP_HERD_X, TOP_HERD_Y - 6 * i))
    for i, card in enumerate(game_board["deck"]):
        if i < 12:
            screen.blit(images["cards"]["back"], (DECK_X + 2 * i, DECK_Y - 4 * i))
    for k, v in game_board["tokens"].items():
        if "x" in k or k == "ca":
            for i, number in enumerate(v):
                screen.blit(images["tokens"][k], (TOKEN_LEFT_X , TOKEN_Y[k] - 6 * i))
        else:
            for i, number in enumerate(v):
                    screen.blit(images["tokens"][k + str(number)], (TOKEN_RIGHT_X - 22 * i , TOKEN_Y[k]))

    for k, v in game_board[top_player]["token_bonus_amount"].items():
        screen.blit(images["tokens"][k], (TOKEN_X + (TOKEN_WIDTH + 20) * (int(k[1]) - 3), TOP_TOKEN_Y))
        draw_text(screen, str(v), SMALL_TEXT_SIZE, (TOKEN_VALUE_X + (TOKEN_WIDTH + 20) * (int(k[1]) - 3)), TOP_TOKEN_VALUE_Y, (0,0,0), True)
    for k, v in game_board[bottom_player]["token_bonus_amount"].items():
        screen.blit(images["tokens"][k], (TOKEN_X + (TOKEN_WIDTH + 20) * (int(k[1]) - 3), BOTTOM_TOKEN_Y))
        draw_text(screen, str(v), SMALL_TEXT_SIZE, (TOKEN_VALUE_X + (TOKEN_WIDTH + 20) * (int(k[1]) - 3)), BOTTOM_TOKEN_VALUE_Y, (0, 0, 0), True)

    draw_text(screen, str(len(game_board["deck"])), MEDIUM_TEXT_SIZE , DECK_SIZE_X, DECK_SIZE_Y,(0,0,0), True)
    draw_text(screen, str(len(game_board[top_player]["herd"])), MEDIUM_TEXT_SIZE , HERD_SIZE_X, TOP_HERD_SIZE_Y,(0,0,0), True)
    draw_text(screen, str(len(game_board[bottom_player]["herd"])), MEDIUM_TEXT_SIZE, HERD_SIZE_X, BOTTOM_HERD_SIZE_Y, (0, 0, 0), True)
    draw_text(screen, str(game_board[top_player]["token_tally"]), LARGE_TEXT_SIZE, TOKEN_TALLY_X, TOP_TOKEN_TALLY_Y,(0, 0, 0), True)
    draw_text(screen, str(game_board[bottom_player]["token_tally"]), LARGE_TEXT_SIZE, TOKEN_TALLY_X, BOTTOM_TOKEN_TALLY_Y,(0, 0, 0), True)

def select_card(surface, COLOR_BORDER, carta, WIDTH_BORDER):
    pygame.draw.rect(surface, COLOR_BORDER, carta, WIDTH_BORDER)

def run_game_ui():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    images_dict = load_images()
    pygame.display.set_caption("Jaipur - Cliente")
    clock = pygame.time.Clock()

    temp = {
        'deck': ['si', 'cl', 'sp', 'di', 'si', 'cl', 'cl', 'le', 'sp', 'si', 'le', 'cl', 'cl', 'ca', 'ca', 'di', 'go',
                 'le',
                 'go', 'ca', 'go', 'si', 'si', 'sp', 'le', 'di', 'ca', 'le', 'sp', 'go', 'go', 'ca', 'le', 'ca', 'sp',
                 'ca',
                 'cl', 'si', 'di', 'le'],
        'market': ['ca', 'ca', 'ca', 'sp', 'di'],
        'tokens': {'di': [5, 5, 5, 7, 7], 'go': [5, 5, 5, 6, 6], 'si': [5, 5, 5, 5, 5], 'cl': [1, 1, 2, 2, 3, 3, 5],
                   'sp': [1, 1, 2, 2, 3, 3, 5], 'le': [1, 1, 1, 1, 1, 1, 2, 3, 4], 'x5': [8, 9, 10, 8, 10],
                   'x4': [4, 4, 5, 5, 6, 6], 'x3': [3, 3, 1, 1, 2, 2, 2], 'ca': [5]},
        'current_player': "player1",
        'player1': {'hand': ['di', 'go', 'cl', 'sp', 'sp'], 'herd': ['ca',"ca","ca","ca",'ca',"ca","ca","ca",'ca',"ca","ca"], 'token_bonus_amount': {'x3': 0, 'x4': 0, 'x5': 0}, 'token_tally': 0},
        'player2': {'hand': ['le', 'le', 'le', 'cl'], 'herd': ['ca',"ca","ca","ca",'ca',"ca","ca","ca",'ca',"ca","ca"], 'token_bonus_amount': {'x3': 0, 'x4': 0, 'x5': 0}, 'token_tally': 0,}}

    running = True

    while running:
        clock.tick(FPS)

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
        draw_board(screen, temp, images_dict, "player2", "player1")

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Para probarlo directamente
if __name__ == '__main__':
    run_game_ui()
