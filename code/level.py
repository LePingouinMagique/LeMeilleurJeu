from settings import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map):  # prndsen paramètre une carte à l'appelle
        self.diplay_surface = pygame.display.get_surface()
        
        #groups
        self.all_sprites = pygame.sprite.Group()
        
        self.collision_sprites = pygame.sprite.Group()
        
        
        #######
        self.setup(tmx_map)
        
    def setup(self,tmx_map):
        for x,y,surf in tmx_map.get_layer_by_name('Terrain').tiles(): # prens les positions x,y et la surface de chaque tuile du calque "Terrain"
            Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,(self.all_sprites,self.collision_sprites))
            
        for obj in tmx_map.get_layer_by_name('Objects'):  # ex <TiledObject[15]: "player">
            if obj.name == "player":
                # print(obj.x)
                # print(obj.y)
                Player((obj.x,obj.y),self.all_sprites, self.collision_sprites)
    
    def run(self,dt):
        self.diplay_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.diplay_surface)
        
        
        
		

	
     