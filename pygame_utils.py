
import time
import pygame
from constants import USE_PYGAME

from constants import HEIGHT, WIDTH

if USE_PYGAME:
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
else:
    WIN = 0

def window_settings():
    pygame.display.set_caption('Chess Snake')

def pygame_render(env):
    env.render()
    time.sleep(0.1) 

def close_pygame():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)