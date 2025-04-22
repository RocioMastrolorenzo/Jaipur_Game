from jaipur import *
import pygame
import sys
import constants

def draw_hand(player):
    for i in player.hand:
        screen.blit(img_placeholder, i.rect.topleft)
def draw_deck(deck):
    for i in deck.deck:
        screen.blit(img_placeholder, i.rect.topleft)


if __name__ == '__main__':


    # hacemos setup
    pygame.init()

    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Jaipur")

    img_placeholder = pygame.image.load("jaipur_card_back.png").convert()
    # colors


    x_center = screen.get_width() // 2
    y_center = screen.get_height() // 2

    # main loop
    clock = pygame.time.Clock()
    running = True

    # initial setup
    deck = Deck()
    player1_name = "a"
    player2_name = "b"
    player1 = Player(player1_name)
    player2 = Player(player2_name)
    deck.shuffle_cards()
    player1.deal_hand(deck)
    player2.deal_hand(deck)
    board = Board(player1, player2, deck)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        screen.fill(constants.BACKGROUND_COLOR)

        draw_deck(deck)
        player1.update_pos()
        draw_hand(player1)
        #draw_opponent_hand()
        #draw_market()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()