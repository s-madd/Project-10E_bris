import pygame
import random
import math
from settings import *

pygame.mixer.init()
class LightSystem:
    def __init__(self, screen_width, screen_height, interface):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dark_layer = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.light_mask = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        
        # Основные параметры
        self.base_radius = 80
        self.base_intensity = 240
        self.current_radius = self.base_radius
        self.target_radius = self.base_radius
        
        # Таймеры и состояния
        self.flicker_timer = 0
        self.light_out_timer = 0
        self.wind_effect_timer = 0
        self.is_light_out = False
        self.is_wind_effect = False
        self.light_enabled = True  # Новый переключатель света
        
        # Настройки эффектов (можно регулировать)
        self.FLICKER_CHANCE = 4 / 100 / FPS    # 0.8% шанс мерцания
        self.LIGHT_OUT_CHANCE = 0.1 / 100 / FPS   # 0.1% шанс погасания
        self.WIND_CHANCE = 0.7 / 100 / FPS       # 0.05% шанс эффекта ветра
        self.SMOOTHNESS = 0.06          # Плавность изменений

        self.interface = interface

        self.fade_animation = None  # 'in' или 'out'
        self.fade_start_time = 0
        self.fade_duration = 0
        self.fade_start_radius = 0
        
    def update_light(self, center_pos):
        current_time = pygame.time.get_ticks()
        self._update_fade_animation()
        

        if not self.light_enabled and self.fade_animation != 'in':
            self._update_light_internal(center_pos, 40, 255)
            return
        
        if not self.fade_animation:
            # Редкое погасание
            if (not self.is_light_out) and random.random() < self.LIGHT_OUT_CHANCE:
                pygame.mixer.Sound("sounds/dark.mp3").play()
                self.is_light_out = True
                self.light_out_duration = random.randint(3000, 6000)
                self.light_out_timer = current_time + self.light_out_duration
                self.target_radius = self.base_radius * 0
                self.interface.add_notification('*слепота...*')

            # Плавное изменение радиуса к целевому
            self.current_radius += (self.target_radius - self.current_radius) * self.SMOOTHNESS

            # Обычное мерцание
            if (random.random() < self.FLICKER_CHANCE) and (not self.is_light_out) and (not self.is_wind_effect):
                self.target_radius = self.base_radius * random.uniform(0.8, 1.2)
    

            # Сверхредкий эффект ветра (затухание)
            if (not self.is_wind_effect) and random.random() < self.WIND_CHANCE:
                self.is_wind_effect = True
                self.wind_duration = random.randint(800, 2000)  # 0.8-1 секунды
                self.wind_timer = current_time + self.wind_duration
                self.saved_target = self.target_radius
                self.target_radius = self.base_radius * 0.3  # Сильное затухание
                self.interface.add_notification('*ветер не на вашей стороне*')
                    
        
            if self.is_wind_effect and (current_time > self.wind_timer):
                self.is_wind_effect = False
                self.target_radius = self.saved_target

            # Восстановление после эффектов
            if self.is_light_out and (current_time > self.light_out_timer):
                self.is_light_out = False
                self.target_radius = self.base_radius
                   
        # Интенсивность затемнения (увеличиваем при эффектах)
        intensity = self.base_intensity
        if self.is_light_out: intensity += 30
        if self.is_wind_effect: intensity += 15
        if intensity > 255: intensity = 255
        
        self._update_light_internal(center_pos, int(self.current_radius), intensity)


    
    def _update_light_internal(self, pos, radius, intensity):
        self.dark_layer.fill((0, 0, 0, intensity))
        self.light_mask.fill((0, 0, 0, 255))
        pygame.draw.circle(self.light_mask, (0, 0, 0, 0), pos, radius)
        
        # Мягкие края
        for r in range(radius, max(radius-15, 0), -1):
            alpha = int(255 * (1 - (radius - r)/15))
            pygame.draw.circle(self.light_mask, (0, 0, 0, alpha), pos, r)
    
    def render(self, surface):
        result = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        result.blit(self.dark_layer, (0, 0))
        result.blit(self.light_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(result, (0, 0))

    def fade_out_light(self, duration=3000):
        """Плавно гасит свет в течение указанного времени"""
        if not self.light_enabled or self.fade_animation == 'out':
            return
            
        self.fade_animation = 'out'
        self.fade_start_time = pygame.time.get_ticks()
        self.fade_duration = duration
        self.fade_start_radius = self.current_radius
        
        # Отключаем другие эффекты
        self.is_light_out = False
        self.is_wind_effect = False

        self.target_radius = 0  # Цель - полное выключение

    def fade_in_light(self, duration=3000):
        """Плавно включает свет в течение указанного времени"""
        if self.light_enabled and self.fade_animation == 'in':
            return
            
        self.light_enabled = True
        self.fade_animation = 'in'
        self.fade_start_time = pygame.time.get_ticks()
        self.fade_duration = duration
        self.fade_start_radius = self.current_radius
        self.target_radius = self.base_radius  # Цель - базовый радиус

    def _update_fade_animation(self):
        """Обновляет анимацию затухания/включения"""
        if not self.fade_animation:
            return
            
        progress = min(1.0, (pygame.time.get_ticks() - self.fade_start_time) / self.fade_duration)
        
        if self.fade_animation == 'out':
            self.current_radius = self.fade_start_radius * (1 - progress)
            if progress >= 1.0:
                self.light_enabled = False
                self.fade_animation = None
                
        elif self.fade_animation == 'in':
            self.current_radius = self.fade_start_radius + (self.base_radius - self.fade_start_radius) * progress
            if progress >= 1.0:
                self.fade_animation = None
