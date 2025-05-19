import pygame
from settings import *

class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width  # Ширина области просмотра
        self.height = height  # Высота области просмотра
        self.world_width = world_width  # Ширина игрового мира
        self.world_height = world_height  # Высота игрового мира
        self.true_x = 0
        self.true_y = 0
        self.smoothness = 0.05  # Коэффициент плавности
    
    def apply(self, entity):
        """Применяет смещение камеры к объекту"""
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        """Применяет смещение камеры к прямоугольнику"""
        return rect.move(self.camera.topleft)
    
    def apply_pos(self, pos):
        """Применяет смещение камеры к позиции"""
        return (pos[0] + self.camera.x, pos[1] + self.camera.y)
    
    def update(self, target):
        """Обновляет позицию камеры с учетом границ мира"""
        # Вычисляем целевые координаты (центрируем камеру на цели)
        target_x = -target.rect.centerx + int(self.width / 2)
        target_y = -target.rect.centery + int(self.height / 2)
        
        # Плавное движение камеры
        self.true_x += (target_x - self.true_x) * self.smoothness
        self.true_y += (target_y - self.true_y) * self.smoothness
        
        # Ограничение по левой границе
        if -self.true_x < 0:
            self.true_x = 0
        # Ограничение по правой границе
        elif -self.true_x > self.world_width - self.width:
            self.true_x = -(self.world_width - self.width)
        
        # Ограничение по верхней границе
        if -self.true_y < 0:
            self.true_y = 0
        # Ограничение по нижней границе
        elif -self.true_y > self.world_height - self.height:
            self.true_y = -(self.world_height - self.height)
        
        self.camera = pygame.Rect(int(self.true_x), int(self.true_y), self.width, self.height)