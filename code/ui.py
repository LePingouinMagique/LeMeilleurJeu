import pygame
from sprites import AnimatedSprite

from settings import *
from random import randint


class UI:
    def __init__(self,font,frames):
        self.display_surf = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        #health
        a = frames['heart']
        zoom = 1.5
        self.hearth_frames = [pygame.transform.scale(i,(i.get_width()*zoom,i.get_height()*zoom)) for i in a]
        self.heart_surf_width = self.hearth_frames[0].get_width()
        self.heart_padding = 5
        self.create_hearts(10)



    def create_hearts(self,amount):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(amount):
            x =10 + heart*(self.heart_surf_width+ self.heart_padding)
            y=10
            Heart((x,y),self.hearth_frames,self.sprites)
    def update(self,dt):
        self.sprites.update(dt)
        self.sprites.draw(self.display_surf)


class Heart(AnimatedSprite):
    def __init__(self,pos,frames,groups):
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self,dt):
        self.frame_index += ANIMATION_SPEED*dt
        if self.frame_index<len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0


    def update(self,dt):
        if self.active:
            self.animate(dt)

        else:
            if randint(0,500) == 4:
                self.active = True
