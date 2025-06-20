import pygame
import time

from settings import *
from base_func import *

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

        self.arrow = LUCIDA_30.render('«', True, (255, 255, 255)) #Стрелка выбора
        self.arrow_rect = self.arrow.get_rect()


        self.scale_factor = 3.0

        self.lightbar = scale_img(pygame.image.load('images/lightbar.png'), self.scale_factor)
        self.lightbar_rect = self.lightbar.get_rect()
        self.lightbar_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status6 = scale_img(pygame.image.load('images/light_status6.png'), self.scale_factor)
        self.light_status6_rect = self.light_status6.get_rect()
        self.light_status6_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status5 = scale_img(pygame.image.load('images/light_status5.png'), self.scale_factor)
        self.light_status5_rect = self.light_status5.get_rect()
        self.light_status5_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status4 = scale_img(pygame.image.load('images/light_status4.png'), self.scale_factor)
        self.light_status4_rect = self.light_status4.get_rect()
        self.light_status4_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status3 = scale_img(pygame.image.load('images/light_status3.png'), self.scale_factor)
        self.light_status3_rect = self.light_status3.get_rect()
        self.light_status3_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status2 = scale_img(pygame.image.load('images/light_status2.png'), self.scale_factor)
        self.light_status2_rect = self.light_status2.get_rect()
        self.light_status2_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        self.light_status1 = scale_img(pygame.image.load('images/light_status1.png'), self.scale_factor)
        self.light_status1_rect = self.light_status1.get_rect()
        self.light_status1_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)


        self.hpbar_scale = 3.5

        self.hpbar = scale_img(pygame.image.load('images/lightbar.png'), self.hpbar_scale)
        self.hpbar_rect = self.hpbar.get_rect()
        self.hpbar_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110)

        self.hpstatus6 = scale_img(pygame.image.load('images/hpbar6.png'), self.hpbar_scale)
        self.hpstatus6_rect = self.hpstatus6.get_rect()
        self.hpstatus6_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110)

        self.hpstatus5 = scale_img(pygame.image.load('images/hpbar5.png'), self.hpbar_scale)
        self.hpstatus5_rect = self.hpstatus5.get_rect()
        self.hpstatus5_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110)

        self.hpstatus4 = scale_img(pygame.image.load('images/hpbar4.png'), self.hpbar_scale)
        self.hpstatus4_rect = self.hpstatus4.get_rect()
        self.hpstatus4_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110)

        self.hpstatus3 = scale_img(pygame.image.load('images/hpbar3.png'), self.hpbar_scale)
        self.hpstatus3_rect = self.hpstatus3.get_rect()
        self.hpstatus3_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110)

        self.hpstatus2 = scale_img(pygame.image.load('images/hpbar2.png'), self.hpbar_scale)
        self.hpstatus2_rect = self.hpstatus2.get_rect()
        self.hpstatus2_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110)

        self.hpstatus1 = scale_img(pygame.image.load('images/hpbar1.png'), self.hpbar_scale)
        self.hpstatus1_rect = self.hpstatus1.get_rect()
        self.hpstatus1_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110)



    def draw_points(self, player):
        # Создание текста с текущим здоровьем
        self.points_bar = LUCIDA_30.render(f'{player.points}', True, HP_BAR_COLOR)
        self.rect_p = self.points_bar.get_rect()

        self.points_img = pygame.image.load('images/points_icon.png')
        self.points_img_rect = self.points_img.get_rect()

        self.points_img_rect.bottomleft = (800, 70)
        
        # Позиционирование в верхнем левом углу
        self.rect_p.bottomleft = (870, 60)
        
        # Отрисовка на экране
        self.screen.blit(self.points_bar, self.rect_p)
        self.screen.blit(self.points_img, self.points_img_rect)



    def draw_menu_text(self):
        self.menu_text1 = LUCIDA_18.render('SPACE - подтвердить выбор', True, MENU_FONT_COLOR)
        self.menu_text2 = LUCIDA_18.render('WASD - управление', True, MENU_FONT_COLOR)
        self.menu_text3 = LUCIDA_18.render('f - ударить', True, MENU_FONT_COLOR)
        self.menu_text4 = LUCIDA_18.render('r - сменить снаряжение', True, MENU_FONT_COLOR)

        self.m_t1_rect = self.menu_text1.get_rect()
        self.m_t2_rect = self.menu_text2.get_rect()
        self.m_t3_rect = self.menu_text3.get_rect()
        self.m_t4_rect = self.menu_text4.get_rect()

        self.m_t1_rect.x = 320
        self.m_t1_rect.y = 650
        self.m_t2_rect.x = 320
        self.m_t2_rect.y = 700
        self.m_t3_rect.x = 280
        self.m_t3_rect.y = 750
        self.m_t4_rect.x = 430
        self.m_t4_rect.y = 750

        self.screen.blit(self.menu_text1, self.m_t1_rect)
        self.screen.blit(self.menu_text2, self.m_t2_rect)
        self.screen.blit(self.menu_text3, self.m_t3_rect)
        self.screen.blit(self.menu_text4, self.m_t4_rect)



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
            notif_surface = LUCIDA_18.render(text, True, (255, 255, 255))
            rect = notif_surface.get_rect()
            rect.bottomleft = (20, bottom_y - i * spacing)
            self.screen.blit(notif_surface, rect)
        


    def light_bar(self, hero):
        self.matchsticks_txt = LUCIDA_30.render(f'- {hero.inventory['matchsticks']['count']}', True, (255, 255, 255))
        self.matchsticks_txt_rect = self.matchsticks_txt.get_rect()
        self.matchsticks_txt_rect.bottomleft = (SCREEN_WIDTH - 125, SCREEN_HEIGHT - 135)

        self.lighter_txt = LUCIDA_30.render(f'- {hero.inventory['lighter']['count']}', True, (255, 255, 255))
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



    def hp_bar(self, hero):
        self.screen.blit(self.hpbar, self.hpbar_rect)
        
        if hero.hp / hero.max_hp <= 0.1:
            self.screen.blit(self.hpstatus1, self.hpstatus1_rect)
        elif hero.hp / hero.max_hp <= 0.25:
            self.screen.blit(self.hpstatus2, self.hpstatus2_rect)
        elif hero.hp / hero.max_hp <= 0.5:
            self.screen.blit(self.hpstatus3, self.hpstatus3_rect)
        elif hero.hp / hero.max_hp <= 0.75:
            self.screen.blit(self.hpstatus4, self.hpstatus4_rect)
        elif hero.hp / hero.max_hp < 1:
            self.screen.blit(self.hpstatus5, self.hpstatus5_rect)
        elif hero.hp / hero.max_hp == 1:
            self.screen.blit(self.hpstatus6, self.hpstatus6_rect)