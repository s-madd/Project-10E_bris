import pygame 
import sys

def events(menu_obj):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #нажатие крестика - выход
             pygame.quit()
             sys.exit()
             

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                menu_obj.switch(-1)
            elif event.key == pygame.K_s:
                menu_obj.switch(+1)
            elif event.key == pygame.K_SPACE:
                menu_obj.select()