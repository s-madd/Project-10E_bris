import pygame 
import settings
import sys

def make_red(image, intensity=0.5):
    red_overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    red_overlay.fill((255, 0, 0, int(255 * intensity)))
    red_image = image.copy()
    red_image.blit(red_overlay, (0, 0), special_flags =pygame.BLEND_MULT)
    return red_image

def turn_l(obj):
    if obj.facing_r:
        obj.facing_r = False
        obj.image = pygame.transform.flip(obj.image, True, False)
        obj.saved_img = pygame.transform.flip(obj.base_image, True, False)


def turn_r(obj):
    if not(obj.facing_r):
        obj.facing_r = True
        obj.image = pygame.transform.flip(obj.image, True, False)
        obj.saved_img = obj.base_image