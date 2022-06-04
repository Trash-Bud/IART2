
import pygame

from constants import HEIGHT, WIDTH

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

def window_settings():
    pygame.display.set_caption('Chess Snake')