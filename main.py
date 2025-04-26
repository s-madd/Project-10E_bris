import pygame
import sys

from hero import Hero
from settings import *
import controls
import menu_controls
from menu import Menu


pygame.init() #инизиализация


clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load('images/icon.png')


hero = Hero(screen)
menu_obj = Menu()

objects = [hero]


def run():
    pygame.display.set_caption('tenebris 0.0.2')
    pygame.display.set_icon(icon)


    #МЕНЮ
    menu_obj.append_option('Начать игру', start_game)
    menu_obj.append_option('Выйти', sys.exit)


    while True:
        screen.fill(MENU_COLOR) #задний фон
        menu_obj.draw_m(screen, 100, 100, 75) #отрисовка 
        pygame.display.flip() #обновление экрана

        menu_controls.events(menu_obj) #обработка событий (клавиш)


def start_game():
    pygame.mouse.set_visible(False)
    menu_active = False

    while True:
        screen.fill(BG_COLOR) #задний фон
        hero.draw() #нарисовать текстурку героя
        pygame.display.flip() #обновление экрана
        clock.tick(FPS) #задать фпс

        controls.events(hero) #обработка событий (клавиш)
        hero.update() 


if __name__ == "__main__":
    run()