import pygame
import sys
import random
import math
import time

from settings import *
from base_func import *

# Инициализация аудиосистемы pygame
pygame.mixer.init()


class Enemy():
    def __init__(self, screen):
        """Инициализация врага с базовыми параметрами"""
        self.screen = screen
        
        # Загрузка и масштабирование изображения врага
        original_image = pygame.image.load('images/enemy.png')
        scale_factor = 0.7
        new_size = (int(original_image.get_width() * scale_factor), 
                    int(original_image.get_height() * scale_factor))
        self.base_image = pygame.transform.scale(original_image, new_size)
        
        # Настройка изображения и позиции
        self.image = self.base_image
        self.saved_img = self.base_image
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(range(1, SCREEN_WIDTH))  # Случайная позиция по X
        self.rect.y = random.choice(range(1, SCREEN_HEIGHT))  # Случайная позиция по Y

        # Флаги движения
        self.m_up = False
        self.m_down = False
        self.m_right = False
        self.m_left = False

        # Базовые параметры врага
        self.alive = True
        self.type = 'enemy'          # Тип объекта для идентификации
        self.moveSpeed = 2           # Скорость передвижения
        self.facing_r = True         # Направление взгляда (вправо/влево)

        # Параметры здоровья и атаки
        self.hp = 40
        self.damage = 1              # Урон за атаку
        self.damage_distance = 40    # Дистанция атаки
        self.attack_speed = 2        # Задержка между атаками (в секундах)
        self.stop_before_atck = 1    # Время простоя после атаки
        self.time_red = 0.5          # Длительность эффекта получения урона

        # Счетчики и таймеры
        self.tick = 0                # Общий счетчик кадров
        self.e_red = 0              # Таймер эффекта получения урона
        self.stoper = 0              # Таймер задержки после атаки
        self.dem_tick = 0            # Счетчик для системы атак

        # Флаги состояний
        self.f_damage = True         # Флаг первой атаки
        self.knockback_active = False  # Активно ли отбрасывание
        self.knockback_force = 0     # Сила отбрасывания
        self.knockback_direction = pygame.math.Vector2(0, 0)  # Направление отбрасывания

        # Прямоугольник для обработки коллизий (немного меньше основного)
        self.collision_rect = self.rect.inflate(-10, -10)

    def draw(self):
        """Отрисовка врага на экране, если он жив"""
        if self.alive:
            self.screen.blit(self.image, self.rect)

    def update(self, enemies):
        """
        Обновление состояния врага каждый кадр
        Args:
            enemies: Список всех врагов для обработки взаимодействий
        """
        # Обновление счетчиков
        self.tick += 1      # Общий счетчик кадров (60 кадров = 1 секунда)
        self.dem_tick += 1  # Счетчик для системы атак
        
        # Уменьшение таймера задержки после атаки
        if self.stoper > 0:
            self.stoper -= 1

        # Сброс эффекта получения урона по таймеру
        if (self.tick >= self.e_red) and self.e_red > 0:
            self.image = self.saved_img
            self.e_red = 0
        
        # Обработка отбрасывания
        if self.knockback_active:
            self.apply_knockback()

        # Проверка на смерть
        if self.hp <= 0:
            self.alive = False
            pygame.mixer.Sound("sounds/enemy_dead.mp3").play()
            enemies.remove(self)

    def apply_knockback(self):
        """Применение эффекта отбрасывания при получении урона"""
        old_pos = self.rect.copy()
        
        # Применение силы отбрасывания
        self.rect.x += self.knockback_direction.x * self.knockback_force
        self.rect.y += self.knockback_direction.y * self.knockback_force
        
        # Постепенное уменьшение силы отбрасывания
        self.knockback_force *= 0.9
        if self.knockback_force < 0.1:
            self.knockback_active = False
            
        # Обновление прямоугольника коллизий
        self.collision_rect.center = self.rect.center

    def check_collisions(self, enemies):
        """
        Проверка и обработка столкновений с другими врагами
        Args:
            enemies: Список всех врагов на уровне
        """
        for enemy in enemies:
            if enemy != self and self.collision_rect.colliderect(enemy.collision_rect):
                # Расчет вектора отталкивания
                dx = self.rect.centerx - enemy.rect.centerx
                dy = self.rect.centery - enemy.rect.centery
                distance = max(1, math.sqrt(dx*dx + dy*dy))
                
                # Применение силы отталкивания
                push_force = 5
                self.rect.x += (dx / distance) * push_force
                self.rect.y += (dy / distance) * push_force
                self.collision_rect.center = self.rect.center

    def chase_player(self, player, enemies):
        """
        Логика преследования игрока
        Args:
            player: Объект игрока для преследования
            enemies: Список всех врагов для обработки коллизий
        """
        old_x, old_y = self.rect.x, self.rect.y

        # Расчет направления к игроку
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        # Поворот модели в сторону игрока
        if dx < 0: 
            turn_l(self)
        else: 
            turn_r(self)

        # Сброс эффекта получения урона по таймеру
        if (self.tick >= self.e_red) and self.e_red > 0:
            player.image = player.saved_img
            self.e_red = 0
        
        # Нормализация вектора направления
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Движение к игроку, если он вне радиуса атаки и нет задержки
        if distance > self.damage_distance and self.stoper == 0:  
            dx = dx / distance
            dy = dy / distance
            self.rect.x += dx * self.moveSpeed
            self.rect.y += dy * self.moveSpeed

        # Обновление прямоугольника коллизий
        self.collision_rect.center = self.rect.center

        # Проверка коллизий с другими врагами
        for enemy in enemies:
            if self.collision_rect.colliderect(enemy.collision_rect) and (enemy != self):
                self.rect.x, self.rect.y = old_x, old_y  # Возврат на предыдущую позицию
                self.collision_rect.center = self.rect.center
                break

        # Дополнительная проверка коллизий
        self.check_collisions(enemies)

        # Сброс флага атаки при отдалении от игрока
        if distance > 55: 
            self.f_damage = True
        
        # Атака игрока при приближении
        if distance <= self.damage_distance and not self.knockback_active:
            player.get_damage(self) 

    def knockback(self, force, direction):
        """
        Активация эффекта отбрасывания
        Args:
            force: Сила отбрасывания
            direction: Направление отбрасывания
        """
        self.knockback_active = True
        self.knockback_force = force
        # Нормализация направления (если вектор не нулевой)
        self.knockback_direction = direction.normalize() if direction.length() > 0 else pygame.math.Vector2(0, 0)

    def get_damage(self, damage, time_red=0.5):
        """
        Обработка получения урона
        Args:
            damage: Количество получаемого урона
            time_red: Длительность визуального эффекта (по умолчанию 0.5 сек)
        """
        self.hp -= damage
        self.image = make_red(self.image, 0.7)  # Визуальный эффект получения урона
        self.e_red = self.tick + time_red * FPS  # Установка таймера эффекта