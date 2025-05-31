import pygame
import sys
import math
import time

from settings import *
import controls

class Interface:
    def __init__(self, screen):
        self.screen = screen
        self.notifications = []

        self.matchsticks_img = pygame.image.load('images/matchsticks.png') #Иконка спичек на лайтбаре
        self.matchsticks_rect = self.matchsticks_img.get_rect()
        self.matchsticks_rect.center = (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150)

        self.lighter_img = pygame.image.load('images/lighter.png') #Иконка зажигалки на лайтбар
        self.lighter_rect = self.lighter_img.get_rect()
        self.lighter_rect.center = (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 75)

        self.arrow = ARIAL_30.render('«', True, (255, 255, 255)) #Стрелка выбора
        self.arrow_rect = self.arrow.get_rect()


        self.scale_factor = 3.0

        self.lightbar = pygame.image.load('images/lightbar.png')
        new_size = (int(self.lightbar.get_width() * self.scale_factor),
                    int(self.lightbar.get_height() * self.scale_factor))
        self.lightbar = pygame.transform.scale(self.lightbar, new_size)
        self.lightbar_rect = self.lightbar.get_rect()
        self.lightbar_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status6 = pygame.image.load('images/light_status6.png')
        new_size = (int(self.light_status6.get_width() * self.scale_factor),
                    int(self.light_status6.get_height() * self.scale_factor))
        self.light_status6 = pygame.transform.scale(self.light_status6, new_size)
        self.light_status6_rect = self.light_status6.get_rect()
        self.light_status6_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status5 = pygame.image.load('images/light_status5.png')
        new_size = (int(self.light_status5.get_width() * self.scale_factor),
                    int(self.light_status5.get_height() * self.scale_factor))
        self.light_status5 = pygame.transform.scale(self.light_status5, new_size)
        self.light_status5_rect = self.light_status5.get_rect()
        self.light_status5_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status4 = pygame.image.load('images/light_status4.png')
        new_size = (int(self.light_status4.get_width() * self.scale_factor),
                    int(self.light_status4.get_height() * self.scale_factor))
        self.light_status4 = pygame.transform.scale(self.light_status4, new_size)
        self.light_status4_rect = self.light_status4.get_rect()
        self.light_status4_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status3 = pygame.image.load('images/light_status3.png')
        new_size = (int(self.light_status3.get_width() * self.scale_factor),
                    int(self.light_status3.get_height() * self.scale_factor))
        self.light_status3 = pygame.transform.scale(self.light_status3, new_size)
        self.light_status3_rect = self.light_status3.get_rect()
        self.light_status3_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status2 = pygame.image.load('images/light_status2.png')
        new_size = (int(self.light_status2.get_width() * self.scale_factor),
                    int(self.light_status2.get_height() * self.scale_factor))
        self.light_status2 = pygame.transform.scale(self.light_status2, new_size)
        self.light_status2_rect = self.light_status2.get_rect()
        self.light_status2_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status1 = pygame.image.load('images/light_status1.png')
        new_size = (int(self.light_status1.get_width() * self.scale_factor),
                    int(self.light_status1.get_height() * self.scale_factor))
        self.light_status1 = pygame.transform.scale(self.light_status1, new_size)
        self.light_status1_rect = self.light_status1.get_rect()
        self.light_status1_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)


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

    def add_notification(self, text):
        self.notifications.append((text, time.time()))

    def update(self):
        current_time = time.time()
        
        spacing = 30
        bottom_y = SCREEN_HEIGHT - 50

        self.notifications = [
            (text, t) for (text, t) in self.notifications if current_time - t < 3
        ]

        for i, (text, t) in enumerate(reversed(self.notifications)):
            notif_surface = ARIAL_18.render(text, True, (255, 255, 255))
            rect = notif_surface.get_rect()
            rect.bottomleft = (20, bottom_y - i * spacing)
            self.screen.blit(notif_surface, rect)
        
    def light_bar(self, hero):
        self.matchsticks_txt = ARIAL_30.render(f'- {hero.inventory['matchsticks']['count']}', True, (255, 255, 255))
        self.matchsticks_txt_rect = self.matchsticks_txt.get_rect()
        self.matchsticks_txt_rect.bottomleft = (SCREEN_WIDTH - 125, SCREEN_HEIGHT - 135)

        self.lighter_txt = ARIAL_30.render(f'- {hero.inventory['lighter']['count']}', True, (255, 255, 255))
        self.lighter_txt_rect = self.matchsticks_txt.get_rect()
        self.lighter_txt_rect.bottomleft = (SCREEN_WIDTH - 125, SCREEN_HEIGHT - 60)


        if hero.current_item == 'matchsticks':
            self.arrow_rect.center = (self.matchsticks_txt_rect.bottomright[0] + 20, self.matchsticks_txt_rect.centery)
        elif hero.current_item == 'lighter':
            self.arrow_rect.center = (self.lighter_txt_rect.bottomright[0] + 20, self.lighter_txt_rect.centery)





        self.screen.blit(self.matchsticks_img, self.matchsticks_rect)
        self.screen.blit(self.matchsticks_txt, self.matchsticks_txt_rect)
        self.screen.blit(self.lighter_img, self.lighter_rect)
        self.screen.blit(self.lighter_txt, self.lighter_txt_rect)
        self.screen.blit(self.arrow, self.arrow_rect)
        self.screen.blit(self.lightbar, self.lightbar_rect)

        if hero.inventory[hero.current_item]['strenght'] / hero.inventory[hero.current_item]['lifetime'] <= 0: 
            self.screen.blit(self.light_status1, self.light_status1_rect)
        elif hero.inventory[hero.current_item]['strenght'] / hero.inventory[hero.current_item]['lifetime'] <= 0.2: 
            self.screen.blit(self.light_status2, self.light_status2_rect)
        elif hero.inventory[hero.current_item]['strenght'] / hero.inventory[hero.current_item]['lifetime'] <= 0.4: 
            self.screen.blit(self.light_status3, self.light_status3_rect)
        elif hero.inventory[hero.current_item]['strenght'] / hero.inventory[hero.current_item]['lifetime'] <= 0.6: 
            self.screen.blit(self.light_status4, self.light_status4_rect)
        elif hero.inventory[hero.current_item]['strenght'] / hero.inventory[hero.current_item]['lifetime'] <= 0.8: 
            self.screen.blit(self.light_status5, self.light_status5_rect)
        elif hero.inventory[hero.current_item]['strenght'] / hero.inventory[hero.current_item]['lifetime'] <= 1: 
            self.screen.blit(self.light_status6, self.light_status6_rect)