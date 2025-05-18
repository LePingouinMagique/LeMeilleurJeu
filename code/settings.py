import pygame, sys
from pygame.math import Vector2 as vector

#0WINDOW_WIDTH, WINDOW_HEIGHT =1600,900
WINDOW_WIDTH, WINDOW_HEIGHT =1920,1080
TITLE = 'game001'
MAX_FPS = 200
TILE_SIZE = 64 # size of tuiles
ANIMATION_SPEED = 6
MANNETTE = False
MAX_CACHED_MAPS = 3

# layers 
Z_LAYERS = {
    'fg':3,
	'bg':0,
    'clouds':1,
    'bg tiles':2,
    'path':3,
    'bg details':4,
    'main':5,
    'water':6,

}
