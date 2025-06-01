import pygame
from settings import *
import random
import math
from base_func import *

class Item():
    def __init__(self, screen):
        self.screen = screen

        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0)) 
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(range(1, WORLD_WIDTH))  # Случайная позиция по X
        self.rect.y = random.choice(range(1, WORLD_HEIGHT))
        
        self.tick = 0


class Matchstick(Item):
    def __init__(self, screen):
        super().__init__(screen)
        
        self.image = scale_img(pygame.image.load('images/matchsticks.png'))

    def update(self, matchsticks, hero, interface):
        dx = hero.rect.centerx - self.rect.centerx
        dy = hero.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < 40:
            matchsticks.remove(self)
            pygame.mixer.Sound('sounds/pick_up.mp3').play()
            interface.add_notification('я буду рад даже этому')
            if hero.inventory['matchsticks']['count'] > 0: hero.inventory['matchsticks']['count'] += 1
            elif (hero.inventory['matchsticks']['count'] == 0) and (hero.inventory['matchsticks']['strenght'] > 0): hero.inventory['matchsticks']['count'] += 1
            elif (hero.inventory['matchsticks']['count'] == 0) and (hero.inventory['matchsticks']['strenght'] == 0):
                hero.inventory['matchsticks']['strenght'] = hero.inventory['matchsticks']['lifetime']
                hero.inventory['matchsticks']['count'] += 1


class Lighter(Item):
    def __init__(self, screen):
        super().__init__(screen)

        self.image = scale_img(pygame.image.load('images/lighter.png'))

    def update(self, lighters, hero, interface):
        dx = hero.rect.centerx - self.rect.centerx
        dy = hero.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < 40:
            lighters.remove(self)
            interface.add_notification('с этим получится прожить чуть подольше')
            pygame.mixer.Sound('sounds/pick_up.mp3').play()
            if hero.inventory['lighter']['count'] > 0: hero.inventory['lighter']['count'] += 1
            elif (hero.inventory['lighter']['count'] == 0) and (hero.inventory['lighter']['strenght'] > 0): hero.inventory['lighter']['count'] += 1
            elif (hero.inventory['lighter']['count'] == 0) and (hero.inventory['lighter']['strenght'] == 0):
                hero.inventory['lighter']['strenght'] = hero.inventory['lighter']['lifetime']
                hero.inventory['lighter']['count'] += 1


class Medkit(Item):
    def __init__(self, screen):
        super().__init__(screen)

        self.image = scale_img(pygame.image.load('images/medkit.png'))

    def update(self, medkits, hero, interface):
        dx = hero.rect.centerx - self.rect.centerx
        dy = hero.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if (distance < 40) and (hero.hp < hero.max_hp):
            medkits.remove(self)
            interface.add_notification(f'переливание крови.. (+{min(hero.max_hp - hero.hp, 10)} hp)')
            pygame.mixer.Sound('sounds/healing.mp3').play()
            hero.hp += min(hero.max_hp - hero.hp, 10)

    
