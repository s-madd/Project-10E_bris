import pygame
import sys
import math

from settings import *
import controls

class Interface:
    def __init__(self, screen):
        self.screen = screen
    def draw_hp(self, screen, player):
        # Создание текста с текущим здоровьем
        self.hp_bar = ARIAL_50.render(f'Здоровье: {player.hp}', True, HP_BAR_COLOR)
        self.rect = self.hp_bar.get_rect()
        
        # Позиционирование в верхнем левом углу
        self.rect.x = 1
        self.rect.y = 1
        
        # Отрисовка на экране
        self.screen.blit(self.hp_bar, self.rect)

    def draw_points(self, screen, player):
        # Создание текста с текущим здоровьем
        self.points_bar = ARIAL_50.render(f'Очки: {player.points}', True, HP_BAR_COLOR)
        self.rect_p = self.points_bar.get_rect()
        
        # Позиционирование в верхнем левом углу
        self.rect_p.x = 700
        self.rect_p.y = 1
        
        # Отрисовка на экране
        self.screen.blit(self.points_bar, self.rect_p)

    def draw_menu_text(self, screen):
        self.menu_text1 = ARIAL_18.render('SPACE - подтвердить выбор', True, MENU_FONT_COLOR)
        self.menu_text2 = ARIAL_18.render('WASD - управление', True, MENU_FONT_COLOR)

        self.m_t1_rect = self.menu_text1.get_rect()
        self.m_t2_rect = self.menu_text2.get_rect()

        self.m_t1_rect.x = 320
        self.m_t1_rect.y = 650
        self.m_t2_rect.x = 320
        self.m_t2_rect.y = 700
        
        self.screen.blit(self.menu_text1, self.m_t1_rect)
        self.screen.blit(self.menu_text2, self.m_t2_rect)

        
