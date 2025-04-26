import pygame 
import sys

def events(hero):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #нажатие крестика - выход
             sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                hero.m_up = True
            elif event.key == pygame.K_s:
                hero.m_down = True
            elif event.key == pygame.K_d:
                hero.m_right = True
            elif event.key == pygame.K_a:
                hero.m_left = True
            
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                hero.m_up = False
            elif event.key == pygame.K_s:
                hero.m_down = False
            elif event.key == pygame.K_d:
                hero.m_right = False
            elif event.key == pygame.K_a:
                hero.m_left = False
            
