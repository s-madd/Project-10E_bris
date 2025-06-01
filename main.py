import pygame
import sys
import math
import os
import random
import subprocess
import base_func

from hero import Hero
from enemy import Enemy
from settings import *
import controls
import menu_controls
from menu import Menu
import light_system
from interface import Interface
from camera import Camera
from items import *
import animations


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
interface = Interface(screen)
light_system = light_system.LightSystem(SCREEN_WIDTH, SCREEN_HEIGHT, interface)


def run():
    """
    Главная функция игры, запускающая главное меню.
    Управляет основным игровым циклом и переходом между меню и игрой.
    """
    # Настройка отображения окна
    pygame.display.set_caption('Tenebris 0.0.8')
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
    background = base_func.create_background(dungeon_texture, WORLD_WIDTH, WORLD_HEIGHT)

    cam = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)

    # Запуск фоновой музыки
    pygame.mixer.music.play(loops=-1) 
    scary_music_f = False
    scary_music = pygame.mixer.Sound('sounds/scary_music.mp3')

    # Настройка параметров спрайтов
    enemies = []


    matchsticks = []
    max_matchsticks_c = 5
    spawn_matchsticks_chance = 3 / 100 / FPS

    lighters = []
    max_lighters_c = 3
    spawn_lighters_chance = 2 / 100 / FPS

    medkits = []
    max_medkits_c = 5
    spawn_medkits_chance = 2 / 100 / FPS

    # Основной игровой циклa
    while True:
        # Обработка управления
        controls.events(hero)
        cam.update(hero)
        hero.update(enemies, WORLD_WIDTH, WORLD_HEIGHT, light_system, interface)
        
        

        # Отрисовка игрового мира
        screen.fill(BG_COLOR)  # Базовый цвет фона
        screen.blit(background, cam.apply_rect(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT)))


        #Изменение шанса спавна и макс кол-во спрайтов в соотвествии с состоянием света
        if light_system.light_enabled == False:
            max_enemies_c = 7
            spawn_enemy_chance = 15 / 100 / FPS
        else:
            max_enemies_c = 4
            spawn_enemy_chance = 8 / 100 / FPS


        # Логика появления врагов
        if (random.random() < spawn_enemy_chance) and (len(enemies) < max_enemies_c):
            enemies.append(Enemy(screen))

        # Обновление и отрисовка врагов
        for enemy in enemies:
            if light_system.light_enabled == False:
                enemy.attack_speed = 1
                enemy.damage = 2
                enemy.moveSpeed = 4
            else:
                enemy.attack_speed = enemy.standart_attack_speed
                enemy.damage = enemy.standart_damage
                enemy.moveSpeed = enemy.standart_moveSpeed
                
            enemy.update(enemies, hero)
            enemy.chase_player(hero, enemies)
            screen.blit(enemy.image, cam.apply(enemy))
        



        if (random.random() < spawn_matchsticks_chance) and (len(matchsticks) < max_matchsticks_c):
            matchsticks.append(Matchstick(screen))

        for matchstick in matchsticks:
            matchstick.update(matchsticks, hero, interface)
            screen.blit(matchstick.image, cam.apply(matchstick))


        if (random.random() < spawn_lighters_chance) and (len(lighters) < max_lighters_c):
            lighters.append(Lighter(screen))

        for lighter in lighters:
            lighter.update(lighters, hero, interface)
            screen.blit(lighter.image, cam.apply(lighter))


        if (random.random() < spawn_medkits_chance) and (len(medkits) < max_medkits_c):
            medkits.append(Medkit(screen))

        for medkit in medkits:
            medkit.update(medkits, hero, interface)
            screen.blit(medkit.image, cam.apply(medkit))
        

        for item in hero.inventory.keys():
            if (hero.inventory[item]['count'] != 0) or (hero.inventory[item]['strenght'] != 0):
                scary_music_f = False
                scary_music.fadeout(5000)
                break
        else:
            if scary_music_f == False:
                scary_music_f = True
                scary_music.play()

        # Отрисовка персонажа
        screen.blit(hero.image, cam.apply(hero))
        animations.attacking_animation(hero, screen, cam)
        
        # Обновление системы освещения
        light_system.update_light(cam.apply_pos(hero.rect.center)) 
        light_system.render(screen)  

        # Отрисовка интерфейса
        interface.draw_hp(screen, hero)
        interface.draw_points(screen, hero)
        interface.light_bar(hero)
        interface.update()
    
        # Обновление экрана
        pygame.display.flip()
        clock.tick_busy_loop(FPS)  # Поддержка заданной частоты кадров

        # Проверка условия поражения
        if hero.hp <= 0:
            break

        
    # Обработка завершения игры
    restart_game = menu.show_death_screen(screen, hero)
    if restart_game:
        pygame.quit()
        os.system("restart.bat")


if __name__ == "__main__":
    run()