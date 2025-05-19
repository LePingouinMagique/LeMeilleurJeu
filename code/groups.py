
import pygame

from settings import *
from sprites import Sprite, Cloud
from random import  choice,randint
from timer import Timer

class AllSprites(pygame.sprite.Group):
    def __init__(self,width,height, clouds,horizon_line,bg_tile= None, top_limit = 0):
        super().__init__()
        self.bg_tiles = bg_tile
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

        self.width, self.height = width*TILE_SIZE, height*TILE_SIZE
        self.borders = {
            'left':0,
            'right': -self.width + WINDOW_WIDTH,
            'bottom':-self.height + WINDOW_HEIGHT,
            'top':top_limit
        }
        self.sky = not bg_tile   #si on doit faire le ciel ou pas
        self.horizon_line = horizon_line

        if bg_tile:
            for col in range(width):
                for row in range(height):
                    x,y = col *TILE_SIZE,row*TILE_SIZE
                    Sprite((x,y),bg_tile,self,0)
        else:
            #sky
            self.large_cloud = clouds['large']
            self.small_cloud = clouds['small']

            self.cloud_direction = -1

            #large
            self.large_cloud_speed = 50
            self.large_cloud_x = 0
            self.large_cloud_tiles = int(self.width/self.large_cloud.get_width()) +2 #nombre de big nuages nécessaires
            self.large_cloud_width, self.large_cloud_height = self.large_cloud.get_size()
            # print(self.large_cloud_tiles)

            #small clouds
            #timer => cloud every 2.5 s.
            #random speed

            self.cloud_timer = Timer(3500, func=self.create_small_clouds, repeat=True)
            self.cloud_timer.activate()
            for cloud in range(10):
                Cloud(pos = (randint(0,self.width),randint(self.borders['top'],self.horizon_line)),
                      surf = choice(self.small_cloud),
                      groups=self)

    def camera_constraint(self):
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']

    def draw_sky(self):
        self.display_surface.fill('#d1c1e6')
        horizon_pos = self.horizon_line + self.offset.y

        sea_rect = pygame.FRect((0,horizon_pos),(WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.draw.rect(self.display_surface,'#92a9ce',sea_rect)

        #ligne horizon
        pygame.draw.line(self.display_surface,'#f5f1de',(0,horizon_pos),(WINDOW_WIDTH,horizon_pos),4)

    def draw_large_cloud(self,dt):
        self.large_cloud_x += self.large_cloud_speed*dt*self.cloud_direction
        if self.large_cloud_x <= - self.large_cloud_width:
            self.large_cloud_x = 0                              #permet de faire une boucle avec les n grands nuages
        for cloud in range(self.large_cloud_tiles):
            left = self.large_cloud_x + cloud*self.large_cloud_width + self.offset.x
            top = self.horizon_line - self.large_cloud_height + self.offset.y
            self.display_surface.blit(self.large_cloud,(left,top))

    def create_small_clouds(self):
        Cloud(pos=(self.width+60, randint(self.borders['top'], self.horizon_line)),
              surf=choice(self.small_cloud),
              groups=self)

    def draw(self,target_pos,dt):
        #target_pos => position du player pour info
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH//2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT//2)
        self.camera_constraint()
        if not self.bg_tiles:
            self.cloud_timer.update()
            self.draw_large_cloud(dt)
        if self.sky:
            self.draw_sky()
        for sprite in sorted(self,key = lambda sprite : sprite.z): #dessine selon lordre des layer donnée par Z_Layer
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            