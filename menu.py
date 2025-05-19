import pygame
import sys
from settings import *
import time


class Menu:
    def __init__(self):
        self._option_surfaces = [] # список поверхностей (строчек меню)
        self._callbacks = [] # список вызванных функций, привязанных к строчке
        self._current_option_idex = 0 # текущая выбранная область меню

    def append_option(self, option, callback): #добавление опции (текст пункта меню, функция)
        self._option_surfaces.append(ARIAL_50.render(option, True, MENU_FONT_COLOR)) #добавление отренд. текста
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
                pygame.draw.rect(surf, MENU_CHNG_BTN_COLOR, option_rect)
            surf.blit(option, option_rect)

    def show_death_screen(self, screen, hero):
        """Функция для отображения экрана смерти"""
    
        screen.fill((0, 0, 0))
        
        # Текст "Вы погибли"
        death_text = ARIAL_50.render("ВЫ ПОГИБЛИ", True, (255, 255, 255))
        death_rect = death_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(death_text, death_rect)
        
        # Инструкция для продолжения
        restart_text = ARIAL_30.render("Нажмите ESC для рестарта", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        screen.blit(restart_text, restart_rect)

        points_text = ARIAL_30.render(f"Заработано {hero.points} очков", True, (255, 255, 255))
        points_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2 + 150))
        screen.blit(points_text, points_rect)
        
        pygame.display.flip()
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Выход из игры
                        return True
        





