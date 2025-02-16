from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        
    def draw(self,target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH//2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT//2)
        for sprite in sorted(self,key = lambda sprite : sprite.z): #dessine selon lordre des layer donnée par Z_Layer
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            