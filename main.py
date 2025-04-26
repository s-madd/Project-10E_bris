import pygame
import sys

from hero import Hero
from settings import *
import controls

def run():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('tenebris 0.0.1')
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    pygame.mouse.set_visible(False)

    hero = Hero(screen)


    while True:
        screen.fill(BG_COLOR) #задний фон
        hero.draw() #нарисовать текстурку героя
        pygame.display.flip() #обновление экрана
        clock.tick(FPS) #задать фпс

        controls.events(hero) #обработка событий (клавиш)
        hero.update()


run()