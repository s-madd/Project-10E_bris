import pygame
import sys
import random
import math
import time

from settings import *
from base_func import *

class Enemy():
    def __init__(self, screen):
        self.screen = screen
        original_image = pygame.image.load('images/enemy.png')

        scale_factor = 0.8
        new_size = (int(original_image.get_width() * scale_factor), 
                    int(original_image.get_height() * scale_factor))
        self.base_image = pygame.transform.scale(original_image, new_size)
        
        self.image = self.base_image
        self.saved_img = self.base_image
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(range(1, SCREEN_WIDTH)) #рандомное появление на карте
        self.rect.y = random.choice(range(1, SCREEN_HEIGHT))

        self.m_up = False
        self.m_down = False
        self.m_right = False
        self.m_left = False
 
        self.type = 'enemy' #тип объекта
        self.moveSpeed = 2 #скорость передвижения
        self.facing_r = True #флаг поворота модели направо
        
        self.damage = 1 #урон
        self.damage_distance = 40 #радиус атаки
        self.attack_speed = 2 #скорость атаки - 2 секунды
        self.stop_before_atck = 1 #время стана после удара
        self.time_red = 0.5 #насколько делает модельку игрока красной

        self.tick = 0 #неизменяемые переменные
        self.e_red = 0
        self.stoper = 0
        self.dem_tick = 0

        self.f_damage = True #флаг при первом соприкосновении с героем - удар


    def draw(self):
        self.screen.blit(self.image, self.rect)


    def update(self):
        self.tick += 1 #общая система тиков. (система тиков: каждое обновление экрана (60 раз в сек) + 1. позволяет отсчитывать на какое время выполнять задержку, не останавливая основную программу)
        self.dem_tick += 1 #система тиков для ударов
        if self.stoper > 0: self.stoper -= 1 #задержка после удара
        

    def chase_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        if dx < 0: 
            turn_l(self)
        else: 
            turn_r(self)

        if (self.tick >= self.e_red) and self.e_red > 0:
            player.image = player.saved_img
            
            self.e_red = 0
        
        # Нормализуем вектор (чтобы скорость была постоянной)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Движение врага (работает всегда)
        if distance > self.damage_distance and self.stoper == 0:  
            dx = dx / distance
            dy = dy / distance
            self.rect.x += dx * self.moveSpeed
            self.rect.y += dy * self.moveSpeed

        if distance > 55: self.f_damage = True
        
        # Логика атаки с задержкой
        if distance <= self.damage_distance:
            
            if (self.dem_tick % (self.attack_speed * FPS) == 0) or self.f_damage == True:
                self.e_red = self.tick + self.time_red * 60
                player.hp -= self.damage

                player.image = make_red(player.image, 0.7)
                self.dem_tick = 0

            self.f_damage = False

            if self.stoper == 0: self.stoper = self.stop_before_atck * FPS               



                

