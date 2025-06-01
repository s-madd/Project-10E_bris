import pygame
import sys
import math
import random

from settings import *
from base_func import *


class Hero:
    def __init__(self, screen):
        """Инициализация главного героя с базовыми параметрами"""
        self.screen = screen
        
        # Загрузка и масштабирование изображения героя
        original_image = pygame.image.load('images/hero.png')
        scale_factor = 0.8
        new_size = (int(original_image.get_width() * scale_factor),
                    int(original_image.get_height() * scale_factor))
        self.base_image = pygame.transform.scale(original_image, new_size)
        
        # Настройка изображения и позиции
        self.image = self.base_image
        self.saved_img = self.base_image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Прямоугольник для обработки коллизий (немного меньше основного)
        self.collision_rect = self.rect.inflate(-10, -10)

        # Флаги управления
        self.m_up = False
        self.m_down = False
        self.m_right = False
        self.m_left = False
        self.is_attacking = False

        # Базовые параметры героя
        self.type = 'hero'           # Тип объекта для идентификации
        self.moveSpeed = 4           # Скорость передвижения
        self.facing_r = True         # Направление взгляда (вправо/влево)
        self.hp = 100            # Здоровье
        self.max_hp = 100
        self.points = 0

        # Параметры атаки
        self.player_radius = 20       # Радиус персонажа
        self.attack_progress = 0      # Прогресс анимации атаки
        self.attack_speed = 0.08      # Скорость анимации атаки
        self.attack_damage = 10       # Урон от атаки
        self.attack_range = 70      # Дистанция атаки
        self.attack_width = 80        # Ширина области атаки

        # Счетчики и флаги
        self.e_red = 0               # Таймер эффекта получения урона
        self.tick = 0                # Общий счетчик кадров
        self.has_dealt_damage = False # Флаг нанесения урона в текущей атаке

        self.inventory = {'matchsticks': {
            'count': 2,
            'strenght': 15,
            'lifetime': 15,
            'empty': False
        },
                          'lighter': {
                              'count': 0, 
                              'strenght': 0,
                              'lifetime': 35,
                              'empty': True
                          }}
        
        self.current_item_index = 0
        self.current_item = 'matchsticks'

        self.light_delay = 0
        self.l_switch = False
        self.firts_light = True


    def update(self, enemies, world_width, world_height, ls, interface):
        self.tick += 1  # Увеличение счетчика кадров. Нужен для реализации задержек без delay

        """Блок освещения"""
        #Изменяем параметры освещения в зависимости от выбранного предмета
        if self.current_item == 'matchsticks':
            ls.base_radius =  80
            ls.base_intensity = 240

        elif self.current_item == 'lighter':
            ls.base_radius = 130
            ls.base_intensity = 220

        #Первая спичка, производим звук
        if self.firts_light:
            pygame.mixer.Sound(f'sounds/{self.current_item}.mp3').play()
            self.firts_light = False 

        #Переключение предмета кнопкой R
        if (self.l_switch == True): 
            self.l_switch = False
            if (self.inventory[self.current_item]['strenght'] > 0) and (self.inventory[self.current_item]['empty'] != True):
                pygame.mixer.Sound(f'sounds/{self.current_item}.mp3').play()
                ls.fade_in_light(500)

            else:
                ls.fade_out_light(100)
                interface.add_notification('я начинаю чувствовать страх..')

        #Флаг empty - пустой инвентарь в категории выбранного предмета. Если инвент пустой, то после нахождения предмета нужно зажечь свет (используется в дальнейшем)
        if (self.inventory[self.current_item]['count'] == 0) and (self.inventory[self.current_item]['strenght'] == 0):
            self.inventory[self.current_item]['empty'] = True
            

        #Логика инструментов освещения
        if (self.inventory[self.current_item]['strenght'] == 0) and (self.inventory[self.current_item]['count'] > 0):
            ls.fade_out_light(100)
            pygame.mixer.Sound('sounds/fade_out.mp3').play()
            if self.inventory[self.current_item]['count'] > 1:
                self.inventory[self.current_item]['count'] -= 1
                self.inventory[self.current_item]['strenght'] = self.inventory[self.current_item]['lifetime']
                self.light_delay = FPS * 1 

            elif self.inventory[self.current_item]['count'] == 1:
                self.inventory[self.current_item]['count'] -= 1
                self.light_delay = FPS * 1
                interface.add_notification('я начинаю чувствовать страх..')

        else:
            if self.tick % FPS == 0:
                if self.inventory[self.current_item]['strenght'] > 0:
                    if self.inventory[self.current_item]['empty'] == True:
                        self.inventory[self.current_item]['empty'] = False
                        pygame.mixer.Sound(f'sounds/{self.current_item}.mp3').play()
                        ls.fade_in_light(500)

                    self.inventory[self.current_item]['strenght'] -= 1


        #Восстановление после затухания
        if self.light_delay > 0:
            self.light_delay -= 1
            if self.light_delay == 0:
                if self.inventory[self.current_item]['count'] > 0:
                    self.inventory[self.current_item]['strenght'] = self.inventory[self.current_item]['lifetime']
                    ls.fade_in_light(500)
                    pygame.mixer.Sound(f'sounds/{self.current_item}.mp3').play()



        """Основной блок"""
        #Очки за время выживания
        if self.tick % (FPS * 10) == 0: self.points += 2

        # Сброс эффекта получения урона по таймеру
        if (self.tick >= self.e_red) and self.e_red > 0:
            self.image = self.saved_img
            self.e_red = 0

        # Обработка движения
        if self.m_up and self.rect.top > 0:
            self.rect.centery -= 1 * self.moveSpeed
        if self.m_down and self.rect.bottom < world_height:
            self.rect.centery += 1 * self.moveSpeed
        if self.m_right and self.rect.right < world_width:
            turn_r(self)
            self.rect.centerx += 1 * self.moveSpeed
        if self.m_left and self.rect.left > 0:
            turn_l(self)
            self.rect.centerx -= 1 * self.moveSpeed

        # Запрет на прохождение границ мира
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > world_width:
            self.rect.right = world_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > world_height:
            self.rect.bottom = world_height

        # Обновление прямоугольника коллизий и обработка атаки
        self.collision_rect.center = self.rect.center
        self.deal_area_damage(enemies)



    def deal_area_damage(self, enemies):
        """
        Нанесение урона врагам в области атаки
        Args:
            enemies: Список всех врагов на уровне
        """
        # Проверка условий для нанесения урона
        if (not self.is_attacking) or (self.attack_progress < 0.3) or (self.attack_progress > 0.6) or self.attack_progress == 0:
            self.has_dealt_damage = False
            return  # Урон наносится только в середине анимации

        if self.has_dealt_damage:
            return  # Урон уже нанесен в этом цикле атаки
        
        self.has_dealt_damage = True
        
        # Определение области атаки (прямоугольник)
        if self.facing_r:
            # Атака вправо
            attack_rect = pygame.Rect(
                self.rect.right,
                self.rect.centery - self.attack_width//2,
                self.attack_range,
                self.attack_width
            )
        else:
            # Атака влево
            attack_rect = pygame.Rect(
                self.rect.left - self.attack_range,
                self.rect.centery - self.attack_width//2,
                self.attack_range,
                self.attack_width
            )

        # Нанесение урона всем врагам в области атаки
        for enemy in enemies[:]:  # Используем копию списка для безопасного изменения
            if attack_rect.colliderect(enemy.rect):
                # Расчет направления отбрасывания
                dx = enemy.rect.centerx - self.rect.centerx
                dy = enemy.rect.centery - self.rect.centery
                direction = pygame.math.Vector2(dx, dy).normalize()

                # Применение отбрасывания и урона
                enemy.knockback(10, direction)
                enemy.get_damage(self.attack_damage)
                

    def get_damage(self, enemy):
        # Расчет расстояния до врага
        dx = self.rect.centerx - enemy.rect.centerx
        dy = self.rect.centery - enemy.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Проверка условий для получения урона
        if distance <= enemy.damage_distance and not enemy.knockback_active:
            # Проверка тайминга атаки врага
            if (enemy.dem_tick % (enemy.attack_speed * FPS) == 0) or enemy.f_damage:
                # Визуальный эффект получения урона
                self.image = make_red(self.image, 0.7)
                self.e_red = self.tick + enemy.time_red * FPS
                
                # Уменьшение здоровья
                self.hp -= enemy.damage
                pygame.mixer.Sound("sounds/scream.mp3").play()
                
                # Сброс параметров врага после атаки
                enemy.f_damage = False
                enemy.dem_tick = 0
                enemy.stoper = enemy.stop_before_atck * FPS
        