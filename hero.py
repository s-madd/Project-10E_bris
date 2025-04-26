import pygame
import sys

from settings import *


class Hero():

    def __init__(self, screen):
        self.screen = screen
        original_image = pygame.image.load('images/hero.png')

        scale_factor = 0.8
        new_size = (int(original_image.get_width() * scale_factor), 
                    int(original_image.get_height() * scale_factor))
        self.base_image = pygame.transform.scale(original_image, new_size)
        
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom #отрисовка

        self.m_up = False
        self.m_down = False
        self.m_right = False
        self.m_left = False
 
        self.type = 'hero' #тип объекта
        self.moveSpeed = 4 #скорость передвижения
        self.facing_r = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.m_up:
            self.rect.centery -= 1 * self.moveSpeed
        if self.m_down:
            self.rect.centery += 1 * self.moveSpeed
        if self.m_right:
            self.turn_r()
            self.rect.centerx += 1 * self.moveSpeed
        if self.m_left:
            self.turn_l()
            self.rect.centerx -= 1 * self.moveSpeed

    def turn_l(self):
        if self.facing_r:
            self.facing_r = False
            self.image = pygame.transform.flip(self.base_image, True, False)

    def turn_r(self):
        if not(self.facing_r):
            self.facing_r = True
            self.image = self.base_image
        

