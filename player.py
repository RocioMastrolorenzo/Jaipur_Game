from logging import raiseExceptions

from card import Card
from gametoken import GameToken
from resource import Resource
import constants

class Player:
    def __init__(self, name):
        self.name: str = name
        self.hand: list[Card] = []
        self.herd: list[Card] = []
        self.token_pile: list[GameToken] = []
        self.token_tally: int = 0
        self.score: int = 0
        self.conn = None

    def __repr__(self):
        s = ''
        for i in self.hand:
            s += str(i) + ' '
        return s

    def deal_hand(self, deck):
        self.hand.extend(deck.deal_cards(5))

    def hide_hand(self):
        hidden_hand = ''
        for i in range(len(self.hand)):
            hidden_hand += '[??] '
        return hidden_hand

    def check_herd(self):
        for i in range(len(self.hand))[::-1]:
            if self.hand[i].card_type == Resource.CAMEL:
                self.herd.append(self.hand.pop(i))

    def sell(self, board, type, amount):

        type = Resource(type)


        # put sold cards on discard pile
        cards_sold = 0
        for i in range(len(self.hand))[::-1]:
            if self.hand[i].card_type == type and cards_sold != amount:
                board.discard_pile.append(self.hand.pop(i))
                cards_sold += 1

        # make amount equal to the amount of tokens left
        if amount > len(board.tokens[type]):
            amount = len(board.tokens[type])

        # get resource tokens
        for i in range(amount):
            self.token_pile.append(board.tokens[type].pop(0))

        # get bonus tokens

        if amount == 3 and len(board.tokens[Resource.TOKENX3]) > 0:
            self.token_pile.append(board.tokens[Resource.TOKENX3].pop(0))

        elif amount == 4 and len(board.tokens[Resource.TOKENX4]) > 0:
            self.token_pile.append(board.tokens[Resource.TOKENX4].pop(0))

        elif amount >= 5 and len(board.tokens[Resource.TOKENX5]) > 0:
            self.token_pile.append(board.tokens[Resource.TOKENX5].pop(0))

    def exchange(self, board, player_card_indices, market_card_indices):

        player_cards_ex = []
        market_cards_ex = []


        for i in market_card_indices[::-1]:
            market_cards_ex.append(board.market.pop(i))
        for i in player_card_indices[::-1]:
            if i == 99:
                player_cards_ex.append(self.herd.pop())
            else:
                player_cards_ex.append(self.hand.pop(i))

        for i in range(len(player_cards_ex)):
            board.market.append(player_cards_ex.pop(0))

        for i in range(len(market_card_indices)):
            self.hand.append(market_cards_ex.pop(0))

    def take_one_resource(self, board, card_index):
        # take the card from the market and put it in the hand
        self.hand.append(board.market.pop(card_index))

    def take_all_camels(self, board):
        for i in range(len(board.market))[::-1]:
            if board.market[i].card_type == Resource.CAMEL:
                self.herd.append(board.market.pop(i))

    def print_token_pile(self):
        s = ''
        for i in self.token_pile:
            s += f'{i.token_type.value} {i.value} '
        return s

    def count_tokens_no_bonus(self):
        #reset tally so it doesn't add up each round and shows real total
        self.token_tally = 0
        for i in self.token_pile:
            if i.token_type not in Resource.bonus_tokens():
                self.token_tally += i.value

    def count_points(self):
        round_score = 0
        for i in self.token_pile:
            round_score += i.value
        return round_score

    def sort_hand(self):
        self.hand.sort(key=lambda card: card.card_type)

    def update_pos(self):
        first_card_pos = (constants.WIDTH // 2) - ((len(self.hand) * constants.CARD_WIDTH + (len(self.hand) - 1) * constants.PADDING) // 2)

        for i, card in enumerate(self.hand):
            card.rect.x = first_card_pos + i * (constants.CARD_WIDTH + constants.PADDING)
            card.rect.y = 853

    def get_bonus_amounts(self):
        bonus_pile = {"x3": 0, "x4": 0, "x5": 0}
        for i in self.token_pile:
            if i.token_type in Resource.bonus_tokens():
                bonus_pile[i.token_type.value] += 1

        return bonus_pile