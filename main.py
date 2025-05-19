import pygame
import sys
import math
import os
import random
import subprocess

from hero import Hero
from enemy import Enemy
from settings import *
import controls
import menu_controls
from menu import Menu
import ls
from interface import Interface
from camera import Camera


# Инициализация основных систем pygame
pygame.init()

# Инициализация аудиосистемы и загрузка музыки
pygame.mixer.init()
pygame.mixer.music.load("sounds/music.mp3")

# Настройка игрового окна
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка игровых ресурсов
try:
    icon = pygame.image.load('images/icon.png')
    dungeon_texture = pygame.image.load('images/dungeon_breaks_texture2.png')
    dungeon_texture = pygame.transform.scale(dungeon_texture, (48, 48))
except pygame.error as e:
    print(f"Ошибка загрузки ресурсов: {e}")
    sys.exit(1)

# Инициализация основных игровых объектов
hero = Hero(screen)
menu = Menu()
light_system = ls.LightSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
interface = Interface(screen)



def run():
    """
    Главная функция игры, запускающая главное меню.
    Управляет основным игровым циклом и переходом между меню и игрой.
    """
    # Настройка отображения окна
    pygame.display.set_caption('Tenebris 0.0.7')
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(True)

    # Настройка пунктов меню
    menu.append_option('Начать игру', start_game)
    menu.append_option('Выйти', sys.exit)

    # Главный цикл меню
    while True:
        # Отрисовка меню
        screen.fill(MENU_COLOR)
        menu.draw_m(screen, 320, 250, 80)  # Параметры: экран, x, y, отступ между пунктами
        
        # Дополнительные элементы интерфейса
        interface.draw_menu_text(screen)
        
        # Обновление экрана
        pygame.display.flip()
        
        # Обработка событий меню
        menu_controls.events(menu)


def start_game():
    """
    Основной игровой цикл.
    Управляет логикой игры, обработкой событий и отрисовкой.
    """
    pygame.mouse.set_visible(False)
    
    # Создание фона из текстуры
    background = create_background(dungeon_texture, WORLD_WIDTH, WORLD_HEIGHT)


    cam = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)

    # Запуск фоновой музыки
    pygame.mixer.music.play() 

    # Настройка параметров врагов
    enemies = []
    max_enemies_c = 1
    spawn_enemy_chance = 0.008

    # Основной игровой цикл
    while True:
        # Обработка управления
        controls.events(hero)
        hero.update(enemies, WORLD_WIDTH, WORLD_HEIGHT)
        cam.update(hero)

        # Отрисовка игрового мира
        screen.fill(BG_COLOR)  # Базовый цвет фона
        screen.blit(background, cam.apply_rect(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT)))

        # Логика появления врагов
        if (random.random() < spawn_enemy_chance) and (len(enemies) < max_enemies_c):
            enemies.append(Enemy(screen))

        # Обновление и отрисовка врагов
        for enemy in enemies:
            enemy.update(enemies)
            enemy.chase_player(hero, enemies)
            screen.blit(enemy.image, cam.apply(enemy))
        
        # Отрисовка персонажа
        screen.blit(hero.image, cam.apply(hero))
        hero.attacking(screen, cam)
        
        # Обновление системы освещения
        light_system.update_light(cam.apply_pos(hero.rect.center)) 
        light_system.render(screen)  

        # Отрисовка интерфейса
        interface.draw_hp(screen, hero)
        interface.draw_points(screen, hero)
    
        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)  # Поддержка заданной частоты кадров

        # Проверка условия поражения
        if hero.hp <= 0:
            break

    # Обработка завершения игры
    restart_game = menu.show_death_screen(screen, hero)
    if restart_game:
        pygame.quit()
        os.system("restart.bat")


def create_background(texture, width, height):
    """
    Создает поверхность фона, заполненную повторяющейся текстурой.
    
    Args:
        texture (pygame.Surface): Текстурная поверхность
        width (int): Ширина фона
        height (int): Высота фона
    
    Returns:
        pygame.Surface: Созданная поверхность фона
    """
    background = pygame.Surface((width, height))
    tex_width, tex_height = texture.get_size()
    
    # Заполнение поверхности текстурой
    for x in range(0, width, tex_width):
        for y in range(0, height, tex_height):
            background.blit(texture, (x, y))
    
    return background


if __name__ == "__main__":
    run()