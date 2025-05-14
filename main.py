import pygame
import sys
import math
import os
import subprocess

from hero import Hero
from enemy import Enemy
from settings import *
import controls
import menu_controls
from menu import Menu
import ls
from interface import Interface


# Инициализация pygame
pygame.init()

# инизиализация и загрузка музыки
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")

# Настройка экрана и таймера
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка и подготовка ресурсов
try:
    icon = pygame.image.load('images/icon.png')
    dungeon_texture = pygame.image.load('images/dungeon_breaks_texture2.png')
    dungeon_texture = pygame.transform.scale(dungeon_texture, (48, 48))
except pygame.error as e:
    print(f"Ошибка загрузки ресурсов: {e}")
    sys.exit(1)

# Создание игровых объектов
hero = Hero(screen)
enemy = Enemy(screen)
menu = Menu()
light_system = ls.LightSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
interface = Interface(screen)

objects = [hero, enemy, menu, light_system, interface]

def run():
    """Основная функция игры, запускает главное меню."""
    # Настройка отображения окна
    pygame.display.set_caption('Tenebris 0.0.5')
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(True)

    # Настройка пунктов меню
    menu.append_option('Начать игру', start_game)
    menu.append_option('Выйти', sys.exit)
    # Главный цикл меню
    while True:
        # Отрисовка
        screen.fill(MENU_COLOR)
        menu.draw_m(screen, 320, 250, 80)  # Параметры: экран, x, y, отступ между пунктами
        pygame.display.flip()

        # Обработка событий меню
        menu_controls.events(menu)


def start_game():
    """Функция запуска основной игры."""
    pygame.mouse.set_visible(False)
    
    # Создание фона из текстуры
    background = create_background(dungeon_texture, SCREEN_WIDTH, SCREEN_HEIGHT)

    # проигрование музыки
    pygame.mixer.music.play() 

    # Игровой цикл
    while True:
        # Обработка ввода
        controls.events(hero)
        hero.update()
        enemy.update()
        enemy.chase_player(hero)
        
        # Отрисовка
        screen.fill(BG_COLOR)  # Заполняем фон базовым цветом 
        screen.blit(background, (0, 0))  # Рисуем текстурированный фон
        
        enemy.draw()
        hero.draw()  # Рисуем персонажа
        
        
        # Обновление и отрисовка освещения
        light_system.update_light(hero.rect.center)  
        light_system.render(screen)  

        interface.draw_hp(screen, hero)
    
        pygame.display.flip()
        clock.tick(FPS)  # Поддерживаем заданную частоту кадров

        if hero.hp <= 0: break

    restart_game = menu.show_death_screen(screen)
    if restart_game:
        pygame.quit()
        os.system("restart.bat")


def create_background(texture, width, height):
    """
    Создаёт поверхность (Surface) заданного размера, заполненную повторяющейся текстурой.
    
    Args:
        texture: Текстурная поверхность pygame
        width: Ширина фона
        height: Высота фона
    
    Returns:
        pygame.Surface: Созданный фон
    """
    background = pygame.Surface((width, height))
    tex_width, tex_height = texture.get_size()
    
    # Заполняем поверхность текстурой, повторяя её по всей площади
    for x in range(0, width, tex_width):
        for y in range(0, height, tex_height):
            background.blit(texture, (x, y))
    
    return background


if __name__ == "__main__":
    run()