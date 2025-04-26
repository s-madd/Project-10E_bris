import pygame
import sys
from settings import *


class Menu:
    def __init__(self):
        self._option_surfaces = [] # список поверхностей (строчек меню)
        self._callbacks = [] # список вызванных функций, привязанных к строчке
        self._current_option_idex = 0 # текущая выбранная область меню

    def append_option(self, option, callback): #добавление опции (текст пункта меню, функция)
        self._option_surfaces.append(ARIAL_50.render(option, True, (0, 0, 255))) #добавление отренд. текста
        self._callbacks.append(callback) #добавляем опцию

    def switch(self, direction): #переключение
        self._current_option_idex = max(0, min(self._current_option_idex + direction, len(self._option_surfaces) - 1))

    def select(self): #выбор
        self._callbacks[self._current_option_idex]()

    def draw_m(self, surf, x, y, option_y_padding): #отрисовка
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)

            if i == self._current_option_idex:
                pygame.draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)




