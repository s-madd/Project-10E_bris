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
            'strenght': 10,
            'lifetime': 10
        },
                          'lighter': {
                              'count': 2, 
                              'strenght': 15,
                              'lifetime': 15
                          }}
        
        self.current_item_index = 0
        self.current_item = 'matchsticks'

        self.light_delay = 0
        self.l_switch = False


        
    def draw(self):
        """Отрисовка героя на экране"""
        self.screen.blit(self.image, self.rect)

    def update(self, enemies, world_width, world_height, ls):
        """
        Обновление состояния героя каждый кадр
        Args:
            enemies: Список всех врагов для обработки взаимодействий
        """
        self.tick += 1  # Увеличение счетчика кадров


        if self.current_item == 'matchsticks':
            ls.base_radius =  80
        elif self.current_item == 'lighter':
            ls.base_radius = 130

        if (self.l_switch == True) and (self.inventory[self.current_item]['strenght'] > 0):
            self.l_switch = False
            ls.fade_in_light(500)

        if self.tick % FPS == 0:
            
            if self.inventory[self.current_item]['count'] > 0:
                if self.inventory[self.current_item]['strenght'] <= 0:
                    ls.fade_out_light(500)

                    self.inventory[self.current_item]['count'] -= 1

                    if self.inventory[self.current_item]['count'] > 0:
                        self.inventory[self.current_item]['strenght'] = self.inventory[self.current_item]['lifetime']
                        self.light_delay = FPS * 1

                    else:
                        pass
                else:
                    self.inventory[self.current_item]['strenght'] -= 1

            else:
                if ls.light_enabled:
                    ls.fade_out_light(500)

        if hasattr(self, 'light_delay'):
            self.light_delay -= 1
            if self.light_delay <= 0:
                ls.fade_in_light(500)
                del self.light_delay  # Удаляем временный атрибут
            
                # Автоматическое включение при появлении новых предметов
                if not hasattr(self, 'light_delay') and \
                    self.inventory[self.current_item]['count'] > 0 and \
                    not ls.light_enabled:
                    ls.fade_in_light(500)
                    self.inventory[self.current_item]['strenght'] = self.inventory[self.current_item]['lifetime']


        


            # if self.inventory[self.current_item]['strenght'] > 0:
            #     self.inventory[self.current_item]['strenght'] -= 1
            # else:
            #     self.inventory[self.current_item]['count'] -= 1
            #     if self.inventory[self.current_item]['count'] > 0:
            #         self.inventory[self.current_item]['strenght'] = self.inventory[self.current_item]['lifetime']

            
                
            

        if self.tick % (FPS * 10) == 0: self.points += 5

        # Сброс эффекта получения урона по таймеру
        if (self.tick >= self.e_red) and self.e_red > 0:
            self.image = self.saved_img
            self.e_red = 0

        old_x, old_y = self.rect.x, self.rect.y

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



    def attacking(self, screen, camera=None):
        """
        Анимация атаки с эффектом частиц с учетом камеры
        Args:
            screen: Поверхность для отрисовки
            camera: Объект камеры (опционально)
        Returns:
            bool: True если анимация активна, False если завершена
        """
        if not self.is_attacking:
            return False
        
        # Обновление прогресса анимации атаки
        self.attack_progress += self.attack_speed
        
        # Завершение анимации при достижении максимума
        if self.attack_progress >= 1:
            self.is_attacking = False
            self.attack_progress = 0
            return False

        # Создание поверхности для частиц с прозрачностью
        particles_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        
        # Определение точки удара (перед персонажем) в мировых координатах
        hit_x = self.rect.centerx + (30 if self.facing_r else -30)
        hit_y = self.rect.centery - 10
        
        # Генерация новых частиц в момент удара (20-40% прогресса анимации)
        if 0.2 < self.attack_progress < 0.4:
            for _ in range(10):  # Создаем 10 частиц за кадр
                # Параметры частицы
                angle = random.uniform(0, math.pi*2)  # Случайное направление
                speed = random.uniform(1, 5)         # Скорость разлета
                size = random.randint(1, 4)          # Размер частицы
                lifetime = random.randint(20, 40)    # Время жизни
                
                # Цвета пыли/осколков
                dust_colors = [
                    (200, 200, 200),  # Светло-серый
                    (150, 150, 150),  # Серый
                    (120, 100, 80),   # Коричневый
                    (80, 70, 60)      # Темно-коричневый
                ]
                color = random.choice(dust_colors)
                
                # Инициализация списка частиц при необходимости
                if not hasattr(self, 'particles'):
                    self.particles = []
                    
                # Добавление новой частицы (в мировых координатах)
                self.particles.append({
                    'world_x': hit_x,  # Храним мировые координаты
                    'world_y': hit_y,
                    'size': size,
                    'color': color,
                    'speed_x': math.cos(angle) * speed,
                    'speed_y': math.sin(angle) * speed,
                    'lifetime': lifetime,
                    'max_lifetime': lifetime
                })

        # Обновление и отрисовка существующих частиц
        if hasattr(self, 'particles'):
            for particle in self.particles[:]:  # Используем копию списка
                # Обновление позиции в мировых координатах
                particle['world_x'] += particle['speed_x']
                particle['world_y'] += particle['speed_y']
                
                # Замедление частиц со временем
                particle['speed_x'] *= 0.95
                particle['speed_y'] *= 0.95
                
                # Уменьшение времени жизни
                particle['lifetime'] -= 1
                
                # Отрисовка частицы с учетом прозрачности
                if particle['lifetime'] > 0:
                    alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
                    color_with_alpha = (*particle['color'], alpha)
                    
                    # Преобразование мировых координат в экранные
                    if camera:
                        screen_x = particle['world_x'] + camera.camera.x
                        screen_y = particle['world_y'] + camera.camera.y
                    else:
                        screen_x = particle['world_x']
                        screen_y = particle['world_y']
                    
                    # Рисуем квадратные частицы (эффект осколков)
                    particle_rect = pygame.Rect(
                        int(screen_x - particle['size']),
                        int(screen_y - particle['size']),
                        particle['size'] * 2,
                        particle['size'] * 2
                    )
                    pygame.draw.rect(
                        particles_surface, 
                        color_with_alpha,
                        particle_rect
                    )
                else:
                    self.particles.remove(particle)
        
        # Наложение частиц на экран
        screen.blit(particles_surface, (0, 0))
        
        return True
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
        """
        Обработка получения урона от врага
        Args:
            enemy: Объект врага, наносящего урон
        """
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

    #def light_items(self):
        