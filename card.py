from Jaipur.resource import Resource
import pygame

class Card:
    def __init__(self, card_type):
        self.card_type: Resource = card_type
        self.rect: pygame.Rect = pygame.Rect(511, 438, 145, 204)
        self.face_up: bool = True

    def __repr__(self):
        return f"[{self.card_type.value}]"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.card_type == other.card_type
        return False

    def __hash__(self):
        return hash(self.card_type)
