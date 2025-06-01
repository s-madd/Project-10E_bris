import pygame
import sys
import math
import os
import random
import subprocess
import base_func

import controls
import menu_controls
import animations
import light_system

from settings import *
from items import *

from interface import Interface
from camera import Camera
from menu import Menu
from hero import Hero
from enemy import Enemy


pygame.init()


# Загрузка игровых ресурсов
try:
    icon = pygame.image.load('images/icon2.png')
    dungeon_texture = pygame.image.load('images/dungeon_breaks_texture2.png')
    dungeon_texture = pygame.transform.scale(dungeon_texture, (48, 48))
except pygame.error as e:
    print(f"Ошибка загрузки ресурсов: {e}")
    sys.exit(1)


"""ИНИЦИАЛИЗАЦИЯ"""
pygame.mixer.init() # Инициализация аудиосистемы и загрузка музыки
pygame.mixer.music.load("sounds/music.mp3")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
menu = Menu()
cam = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)
interface = Interface(screen)

light_sys = light_system.LightSystem(SCREEN_WIDTH, SCREEN_HEIGHT, interface)

hero = Hero(screen)

clock = pygame.time.Clock()



def run():
    """ОКНО"""
    pygame.display.set_caption('Tenebris 0.1.0')
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(True)


    """МЕНЮ"""
    # Настройка пунктов меню
    menu.append_option('Начать игру', start_game)
    menu.append_option('Выйти', sys.exit)

    while True:
        # Отрисовка меню
        screen.fill(MENU_COLOR)
        menu.draw_m(screen, 320, 250, 80)  # Параметры: экран, x, y, отступ между пунктами
        
        # Дополнительные элементы интерфейса
        interface.draw_menu_text()
        
        # Обновление экрана
        pygame.display.flip()
        
        # Обработка событий меню
        menu_controls.events(menu)



def start_game():
    """НАЧАЛЬНЫЙ БЛОК"""
    pygame.mouse.set_visible(False)

    # Запуск фоновой музыки
    pygame.mixer.music.play(loops=-1) 
    scary_music_f = False
    scary_music = pygame.mixer.Sound('sounds/scary_music.mp3')

    background = base_func.create_background(dungeon_texture, WORLD_WIDTH, WORLD_HEIGHT)


    """ПАРАМЕТРЫ СПРАЙТОВ"""
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


    # Основной игровой цикл
    while True:
        """НАЧАЛЬНЫЙ БЛОК"""
        screen.fill(BG_COLOR)  # Базовый цвет фон
        controls.events(hero) # Обработка управления


        """ОБНОВЛЕНИЕ ИГРОВЫХ ЭЛЕМЕНТОВ"""
        cam.update(hero) #Обновление камеры
        hero.update(enemies, WORLD_WIDTH, WORLD_HEIGHT, light_sys, interface) #Обновление персонажа
        light_sys.update_light(cam.apply_pos(hero.rect.center)) #Обновление света

        #Изменение шанса спавна и макс кол-во спрайтов в соотвествии с состоянием света
        if light_sys.light_enabled == False:
            max_enemies_c = 7
            spawn_enemy_chance = 15 / 100 / FPS
        else:
            max_enemies_c = 4
            spawn_enemy_chance = 8 / 100 / FPS


        #Спавн игровых элементов
        if (random.random() < spawn_enemy_chance) and (len(enemies) < max_enemies_c):
            enemies.append(Enemy(screen))

        if (random.random() < spawn_matchsticks_chance) and (len(matchsticks) < max_matchsticks_c):
            matchsticks.append(Matchstick(screen))

        if (random.random() < spawn_lighters_chance) and (len(lighters) < max_lighters_c):
            lighters.append(Lighter(screen))

        if (random.random() < spawn_medkits_chance) and (len(medkits) < max_medkits_c):
            medkits.append(Medkit(screen))


        #Обновлние звуковых элементов
        for item in hero.inventory.keys():
            if (hero.inventory[item]['count'] != 0) or (hero.inventory[item]['strenght'] != 0):
                scary_music_f = False
                scary_music.fadeout(5000)
                break
        else:
            if scary_music_f == False:
                scary_music_f = True
                scary_music.play()


        """БЛОК ОТРИСОВКИ"""
        screen.blit(background, cam.apply_rect(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT))) #Фон

        for medkit in medkits:
            medkit.update(medkits, hero, interface)
            screen.blit(medkit.image, cam.apply(medkit)) #Аптечки

        for lighter in lighters:
            lighter.update(lighters, hero, interface)
            screen.blit(lighter.image, cam.apply(lighter)) #Зажигалки

        for matchstick in matchsticks:
            matchstick.update(matchsticks, hero, interface)
            screen.blit(matchstick.image, cam.apply(matchstick)) #Спички

        for enemy in enemies:
            if light_sys.light_enabled == False:
                enemy.attack_speed = 1
                enemy.damage = 2
                enemy.moveSpeed = 4
            else:
                enemy.attack_speed = enemy.standart_attack_speed
                enemy.damage = enemy.standart_damage
                enemy.moveSpeed = enemy.standart_moveSpeed
                
            enemy.update(enemies, hero)
            enemy.chase_player(hero, enemies)
            screen.blit(enemy.image, cam.apply(enemy)) #Враги

        screen.blit(hero.image, cam.apply(hero)) #Герой
        animations.attacking_animation(hero, screen, cam) #Отрисовка анимаций атаки героя

        # Обновление системы освещения
        light_sys.render(screen)  

        # Отрисовка интерфейса
        interface.draw_points(hero)
        interface.light_bar(hero)
        interface.hp_bar(hero)
        interface.update()
    

        """КОНЕЧНЫЙ БЛОК"""
        pygame.display.flip() # Обновление экрана
        clock.tick_busy_loop(FPS)  # Поддержка заданной частоты кадров

        if hero.hp <= 0: # Проверка условия поражения
            break 

        
    restart_game = menu.show_death_screen(screen, hero) # Обработка завершения игры
    if restart_game:
        pygame.quit()
        os.system("restart.bat")


if __name__ == "__main__":
    run()