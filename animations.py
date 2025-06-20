import pygame
from settings import *
import random
import math



def die_animation(obj, enemies):
    """"Обязательно наличие следующих переменных:
    self.is_dying = ...
    self.death_timer = ...
    self.dissolve_level = ...
    self.original_image = ...
    self.image = ...
    self.rect = ...
    """

    obj.is_dying = True
    obj.death_timer = 0
    obj.dissolve_level = 0  # Уровень "растворения" (0-100%)
    
    # Сохраняем оригинальные параметры
    if not hasattr(obj, 'original_image'):
        obj.original_image = obj.image.copy()
    
    def update_dissolve(instance):
        obj.death_timer += 1
        progress = obj.death_timer / FPS  # 1 секунда анимации при 60 FPS
        
        # 1. Эффект "проваливания" - смещение вниз с замедлением
        obj.rect.y += int(5 * (1 - progress**2))
        
        # 2. Эффект "растворения" - постепенное исчезновение снизу вверх
        obj.dissolve_level = min(100, progress * 120)  # Ускоряем растворение
        
        # Создаем маску растворения
        dissolve_height = int(obj.original_image.get_height() * (1 - obj.dissolve_level/100))
        if dissolve_height > 0:
            obj.image = obj.original_image.subsurface(
                (0, 0, obj.original_image.get_width(), dissolve_height))
        else:
            obj.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        
        # 3. Мигание красным в первой половине анимации
        if progress < 0.5 and obj.death_timer % 8 < 4:
            temp_img = obj.image.copy()
            temp_img.fill((255, 50, 50, 150), special_flags=pygame.BLEND_RGBA_ADD)
            obj.image = temp_img
        
        # 4. Завершение анимации
        if obj.death_timer >= FPS:
            enemies.remove(obj)
            return True
        
        return False
    
    # Заменяем метод update
    obj.update = lambda *args: update_dissolve(obj)



def attacking_animation(obj, screen, camera=None): #Анимация частиц при атаке
    """Обязательно наличие следующих переменных:
    self.is_attacking = ...
    self.attack_progress = ...
    self.attack_speed = ...
    self.facing_r = ...
    self.rect = ...
    self.particles = ...
    """

    if not obj.is_attacking:
        return False
    
    # Обновление прогресса анимации атаки
    obj.attack_progress += obj.attack_speed
    
    # Завершение анимации при достижении максимума
    if obj.attack_progress >= 1:
        obj.is_attacking = False
        obj.attack_progress = 0
        return False

    # Создание поверхности для частиц с прозрачностью
    particles_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    
    # Определение точки удара (перед персонажем) в мировых координатах
    hit_x = obj.rect.centerx + (30 if obj.facing_r else -30)
    hit_y = obj.rect.centery - 10
    
    # Генерация новых частиц в момент удара (20-40% прогресса анимации)
    if 0.2 < obj.attack_progress < 0.4:
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
            if not hasattr(obj, 'particles'):
                obj.particles = []
                
            # Добавление новой частицы (в мировых координатах)
            obj.particles.append({
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
    if hasattr(obj, 'particles'):
        for particle in obj.particles[:]:  # Используем копию списка
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
                obj.particles.remove(particle)
    
    # Наложение частиц на экран
    screen.blit(particles_surface, (0, 0))
    
    return True



def vampire_blood_effect(hero, screen, camera=None, target_enemy=None):
    """
    Эффект крови с частицами, летящими в сторону врага
    """
    # Инициализация при первом вызове
    if not hasattr(hero, 'blood_particles'):
        hero.blood_particles = []
    
    # Если эффект не активен - очищаем частицы
    if not getattr(hero, 'blood_effect_active', False):
        hero.blood_particles = []
        return
    
    # Параметры эффекта
    particles_per_frame = 8
    max_particles = 120
    base_radius = 3
    
    # Генерация новых частиц
    for _ in range(particles_per_frame):
        if len(hero.blood_particles) < max_particles:
            # Базовые параметры частицы
            angle = random.uniform(0, 2*math.pi)
            distance = random.uniform(20, 50)
            
            # Начальная позиция вокруг героя
            world_x = hero.rect.centerx + math.cos(angle) * distance
            world_y = hero.rect.centery + math.sin(angle) * distance
            
            # Направление движения (к врагу или случайное)
            if target_enemy and hasattr(target_enemy, 'rect'):
                # Вектор к врагу
                dx = target_enemy.rect.centerx - world_x
                dy = target_enemy.rect.centery - world_y
                dist_to_enemy = math.sqrt(dx*dx + dy*dy)
                
                if dist_to_enemy > 0:
                    # Основное направление к врагу + случайное отклонение
                    direction_strength = 0.7  # Сила притяжения к врагу (0-1)
                    random_strength = 0.3      # Сила случайного движения
                    
                    speed_x = (dx/dist_to_enemy)*direction_strength + (random.random()-0.5)*random_strength
                    speed_y = (dy/dist_to_enemy)*direction_strength + (random.random()-0.5)*random_strength
                    
                    # Нормализуем скорость
                    speed_length = math.sqrt(speed_x*speed_x + speed_y*speed_y)
                    if speed_length > 0:
                        speed_x = speed_x / speed_length * 2.5
                        speed_y = speed_y / speed_length * 2.5
            else:
                # Случайное направление, если враг не указан
                speed_x = (random.random() - 0.5) * 1.5
                speed_y = (random.random() - 0.5) * 1.5 - 0.5
            
            hero.blood_particles.append({
                'world_x': world_x,
                'world_y': world_y,
                'radius': random.uniform(base_radius, base_radius*1.5),
                'color': (
                    random.randint(200, 255),
                    random.randint(0, 30),
                    random.randint(0, 30),
                    random.randint(150, 200)
                ),
                'speed_x': speed_x,
                'speed_y': speed_y,
                'life': random.randint(50, 80),
                'max_life': 80
            })
    
    # Отрисовка
    particles_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    
    for particle in hero.blood_particles[:]:
        # Обновление позиции
        particle['world_x'] += particle['speed_x']
        particle['world_y'] += particle['speed_y']
        particle['life'] -= 1
        
        # Прозрачность и размер
        life_ratio = particle['life'] / particle['max_life']
        alpha = int(particle['color'][3] * life_ratio)
        current_radius = particle['radius'] * (0.3 + 0.7*life_ratio)  # Плавное уменьшение
        
        # Отрисовка
        if particle['life'] > 0:
            # Преобразование координат
            if camera:
                screen_x = particle['world_x'] + camera.camera.x
                screen_y = particle['world_y'] + camera.camera.y
            else:
                screen_x = particle['world_x']
                screen_y = particle['world_y']
            
            pygame.draw.circle(
                particles_surface,
                (particle['color'][0], particle['color'][1], particle['color'][2], alpha),
                (int(screen_x), int(screen_y)),
                max(1, int(current_radius))
            )
        else:
            hero.blood_particles.remove(particle)
    
    screen.blit(particles_surface, (0, 0))