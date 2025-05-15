import random
import json

from card import Card
from deck import Deck
from player import Player
from resource import Resource
from gametoken import GameToken


def custom_serializer(obj):
    if isinstance(obj, Card):
        return obj.card_type.value
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

class Board:
    def __init__(self, p1, p2, deck):
        self.align_offset = 30

        self.tokens: dict[Resource, list[GameToken]] = self.create_tokens()
        self.p1: Player = p1
        self.p2: Player = p2
        self.deck: Deck = deck
        self.market: list[Card] = self.deck.deal_market_setup()
        self.discard_pile: list[Card] = []
        self.current_player: Player = p1
        self.other_player: Player = p2

        self.shuffle_bonus_tokens()


    # noinspection PyMethodMayBeStatic
    def create_tokens(self):
        token_mapping = {
            Resource.DIAMOND: [5, 5, 5, 7, 7],
            Resource.GOLD: [5, 5, 5, 6, 6],
            Resource.SILVER: [5, 5, 5, 5, 5],
            Resource.CLOTH: [1, 1, 2, 2, 3, 3, 5],
            Resource.SPICES: [1, 1, 2, 2, 3, 3, 5],
            Resource.LEATHER: [1, 1, 1, 1, 1, 1, 2, 3, 4],
            Resource.TOKENX5: [10, 10, 9, 8, 8],
            Resource.TOKENX4: [6, 6, 5, 5, 4, 4],
            Resource.TOKENX3: [3, 3, 2, 2, 2, 1, 1],
            Resource.CAMEL: [5],
        }

        tokens = {
            Resource.DIAMOND: [],
            Resource.GOLD: [],
            Resource.SILVER: [],
            Resource.CLOTH: [],
            Resource.SPICES: [],
            Resource.LEATHER: [],
            Resource.TOKENX5: [],
            Resource.TOKENX4: [],
            Resource.TOKENX3: [],
            Resource.CAMEL: [],
        }

        for i in token_mapping:
            for j in token_mapping[i]:
                tokens[i].append(GameToken(i, j))

        return tokens

    def print_tokens(self, resource_type):
        s = ''
        for i in self.tokens[resource_type]:
            s += str(i) + ' '
        return s

    def print_market(self):
        s = ''
        for i in self.market:
            s += f"{i} "
        return s

    def shuffle_bonus_tokens(self):
        for i in Resource.bonus_tokens():
            random.shuffle(self.tokens[i])

    def fill_market(self):
        fill_amount = 5 - len(self.market)
        if len(self.market) < 5:
            self.market.extend(self.deck.deal_cards(fill_amount))

    def switch_players(self):
        temp = self.current_player
        self.current_player = self.other_player
        self.other_player = temp

    def round_end_check(self):
        empty_token_pile = 0
        for i in self.tokens:
            if len(self.tokens[i]) == 0 and i in Resource.normal_resources():
                empty_token_pile += 1

        if empty_token_pile >= 3:
            return True
        elif len(self.market) + len(self.deck) < 5:
            return True
        else:
            return False

    def give_camel_token(self):
        if len(self.p1.herd) != len(self.p2.herd):
            winner = max([self.p1, self.p2], key=lambda p: len(p.herd))
            winner.token_pile.append(self.tokens[Resource.CAMEL].pop())

    def give_point(self):
        if self.p1.count_points() != self.p2.count_points():
            winner = max([self.p1, self.p2], key=lambda p: p.count_points())
            winner.score += 1
            winner = winner.name # to return a string, not a player object repr
        else:
            winner = "Tie    "
        return winner



    def jsonify(self):
        d = {
            "deck" : self.deck.deck,
            "market" : self.market,
            "tokens" : self.tokens_to_dict(),
            "current_player" : self.current_player.name,
            "player1": {
                "hand" : self.p1.hand ,
                "herd" : self.p1.herd ,
                "token_pile" : self.p1.get_bonus_amounts(),
                "token_tally" : self.p1.token_tally ,
            } ,
            "player2": {
                "hand" : self.p2.hand ,
                "herd" : self.p2.herd ,
                "token_pile" : self.p2.get_bonus_amounts(),
                "token_tally" : self.p2.token_tally,
            }
        }
        return json.dumps(d, default=custom_serializer)

    def tokens_to_dict(self):
        res = {}

        for key in self.tokens:
            res[key.value] = []
            for tok in self.tokens[key]:
                res[key.value].append(tok.value)

        return res

    def game_end_check(self):
        return self.p1.score == 2 or self.p2.score == 2

    def __repr__(self):
        s = ""
        blank_line = " " * 104 + "\n"

        s += "+" + "-" * 104 + "+" + "\n"
        s += f'{" " * self.align_offset}{'Opponent hand: ' + self.other_player.hide_hand()}\n'
        s += blank_line
        s += f'{'Opponent herd: ' + str(len(self.other_player.herd)) :^104}\n'
        s += f'{'Deck: ' + str(len(self.deck)):^104}\n'
        s += f'{"Tokens: " + str(len(self.other_player.token_pile)):>104}\n'
        s += f'{"Current points: " + str(self.other_player.count_tokens_no_bonus()):>104}\n'
        s += blank_line
        for resource in Resource.normal_resources():
            temp_s = ''
            temp_s += f' ({resource.value}) {self.print_tokens(resource)}'
            s += temp_s + ' ' * (105 - len(temp_s)) + '\n'
        s += f'{" " * (self.align_offset + 10)}{self.print_market()}\n'
        for resource in Resource.bonus_tokens():
            temp_s = ''
            temp_s += f' ({resource.value}) {self.print_tokens(resource)}'
            s += temp_s + ' ' * (105 - len(temp_s)) + '\n'
        s += blank_line
        s += f'{"Tokens: " + str(len(self.current_player.token_pile)):>104}\n'
        s += f'{"Current points: " + str(self.current_player.count_tokens_no_bonus()):>104}\n'
        s += f'{'Your herd: ' + str(len(self.current_player.herd)) :^104}\n'
        s += blank_line
        s += f'{" " * self.align_offset}{'Your hand: ' + str(self.current_player)}\n'
        s += "+" + "-" * 104 + "+" + "\n"
        return s


