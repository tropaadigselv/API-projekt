#taget fra https://stackoverflow.com/questions/71279888/how-can-i-zoom-into-an-object-and-follow-that-object-in-pygame
# dog modifiseret til mit projekt

import pygame
from pygame.locals import *
import random

# --- constants --- (UPPER_CASE_NAMES)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

FPS = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- main ---

pygame.init()

screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
screen_rect = screen.get_rect()

surface = pygame.surface.Surface( (SCREEN_WIDTH, SCREEN_HEIGHT) )

# --- objects ---

bg_image = pygame.image.load('API projekt\API-projekt\map.png').convert()
bg_image = pygame.transform.rotozoom(bg_image,0,0.28)
bg_rect  = bg_image.get_rect(center=screen_rect.center)

player_image = pygame.image.load("API projekt\API-projekt\plane_icon.png").convert()
player_image = pygame.transform.rotozoom(player_image,0,0.02)
player_rect  = player_image.get_rect(center=screen_rect.center) 

# --- mainloop ---

clock = pygame.time.Clock()

follow_player = False
zoom = True
scale = 1
moving = False
#number = 0  # to generate images for animated `gif` 
# `ffmpeg -i image-%03d.jpg -vf scale=250:200 video.gif`

running = True
while running:

    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOUSEWHEEL:
            if event.y > 0:
                scale = scale+0.05
            elif event.y < 0:
                scale = scale-0.05
        if event.type == MOUSEBUTTONDOWN:
            if bg_rect.collidepoint(event.pos):
                moving = True
        elif event.type == MOUSEBUTTONUP:
            moving = False
        if event.type == MOUSEMOTION and moving:
            #player_rect.move_ip(event.rel)
            bg_rect.move_ip(event.rel)


    # --- draw on surface ---

    surface.fill(BLACK)
    surface.blit(bg_image, bg_rect)
    surface.blit(player_image, player_rect)

    # --- modify surface ---
    
    surface_mod = surface.copy()
    surface_mod_rect = surface_mod.get_rect()

    if zoom:
        surface_mod = pygame.transform.rotozoom(surface_mod, 0, scale)
        surface_mod_rect = surface_mod.get_rect()
        
    surface_mod_rect.x = (screen_rect.centerx - player_rect.centerx*scale)
    surface_mod_rect.y = (screen_rect.centery - player_rect.centery*scale)

    # --- draw surface on screen ---
    
    screen.fill(BLACK)

    screen.blit(surface_mod, surface_mod_rect)
    
    pygame.display.flip()
    clock.tick(FPS)
    
    #pygame.image.save(screen, f"image-{number:03}.jpg")   
    #number += 1

# --- end ---

pygame.quit()