import pygame
import sys
import math

from settings import *
import controls

class Interface:
    def __init__(self, screen):
        self.screen = screen
    def draw_hp(self, screen, player):
        self.hp_bar = ARIAL_50.render(f'Здоровье: {player.hp}', True, HP_BAR_COLOR)
        self.rect = self.hp_bar.get_rect()
        self.rect.x = 1
        self.rect.y = 1
        self.screen.blit(self.hp_bar, self.rect)


        
