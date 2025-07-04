import pygame 


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



def create_background(texture, width, height):
    """
    Создает поверхность фона, заполненную повторяющейся текстурой.
    
    Args:
        texture (pygame.Surface): Текстурная поверхность
        width (int): Ширина фона
        height (int): Высота фона
    
    Returns:
        pygame.Surface: Созданная поверхность фона
    """
    background = pygame.Surface((width, height))
    tex_width, tex_height = texture.get_size()
    
    # Заполнение поверхности текстурой
    for x in range(0, width, tex_width):
        for y in range(0, height, tex_height):
            background.blit(texture, (x, y))
    
    return background



def scale_img(image, scale_factor):
    new_size = (int(image.get_width() * scale_factor), 
                int(image.get_height() * scale_factor))
    return pygame.transform.scale(image, new_size)