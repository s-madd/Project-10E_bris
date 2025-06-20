import pygame
import sys
import os
import random
import base_func

import controls
import menu_controls
import animations
import light_system
import sprites

from settings import *
from items import *

from interface import Interface
from camera import Camera
from menu import Menu
from hero import Hero


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
    pygame.display.set_caption('Tenebris 0.1.1')
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
    hounds = []
    ghouls = []

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
            max_hound_c = 7
            spawn_hound_chance = 15 / 100 / FPS

            max_ghoul_c = 4
            spawn_ghoul_chance = 5 / 100 / FPS
        else:
            max_hound_c = 4
            spawn_hound_chance = 8 / 100 / FPS

            max_ghoul_c = 2
            spawn_ghoul_chance = 2 / 100 / FPS


        #Спавн игровых элементов
        if (random.random() < spawn_hound_chance) and (len(hounds) < max_hound_c):
            hounds.append(sprites.Hound(screen))
            
        if (random.random() < spawn_ghoul_chance) and (len(ghouls) < max_ghoul_c):
            ghouls.append(sprites.Ghoul(screen))

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

        enemies = hounds + ghouls
        for enemy in enemies:
            if light_sys.light_enabled == False:
                enemy.attack_speed = enemy.dark_attack_speed
                enemy.damage = enemy.dark_damage
                enemy.moveSpeed = enemy.dark_moveSpeed
            else:
                enemy.attack_speed = enemy.base_attack_speed
                enemy.damage = enemy.base_damage
                enemy.moveSpeed = enemy.base_moveSpeed
            
            if enemy.type == 'hound': 
                enemy.update(hounds, hero)
                enemy.chase_player(hero, hounds)
            elif enemy.type == 'ghoul':
                enemy.update(ghouls, hero) 
                enemy.chase_player(hero, ghouls)
                animations.vampire_blood_effect(hero, screen, cam, enemy)

            screen.blit(enemy.image, cam.apply(enemy)) 


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