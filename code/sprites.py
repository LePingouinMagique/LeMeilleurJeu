from settings import *


class Sprite(pygame.sprite.Sprite): #pour chaque sprite du groupe qu'on lui donne
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE)) #cration d'uen nouvelle surface
        self.image.fill('white')
        self.rect = self.image.get_frect(topleft = pos)
        
        self.old_rect = self.rect.copy()
        


  