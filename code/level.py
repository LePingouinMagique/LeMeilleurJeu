from settings import *
from sprites import Sprite, MovingSprite
from player import Player
from groups import AllSprites

class Level:
    def __init__(self, tmx_map):  # prndsen paramètre une carte à l'appelle
        self.diplay_surface = pygame.display.get_surface()
        
        #groups
        self.all_sprites = AllSprites()
        
        self.collision_sprites = pygame.sprite.Group()
        
        
        #######
        self.setup(tmx_map)
        
    def setup(self,tmx_map):
        
        for layer in ['BG','Terrain','FG','Platforms']:
            #tiles
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles(): # prens les positions x,y et la surface de chaque tuile du calque "Terrain"
                
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)    # sprite avec les quels il y a de la collision !
                if layer == 'Platforms': groups.append(self.collision_sprites)
                #Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,(self.all_sprites,self.collision_sprites))
                Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,groups)
                
        # for obj in tmx_map.get_layer_by_name('hite'):
        #     groups = [self.all_sprites, self.collision_sprites]  # Collision activée
        #     zz = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
        #     Sprite((obj.x, obj.y), zz, groups)  # Position et image de l'objet
        
        
        for obj in tmx_map.get_layer_by_name('Objects'):  # ex <TiledObject[15]: "player">
            if obj.name == "player":
                # print(obj.x)
                # print(obj.y)
                self.player = Player((obj.x,obj.y),self.all_sprites, self.collision_sprites)

        #moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            #1)  Movings platforms
            if obj.name == 'helicopter':
                if obj.width > obj.height: #horizontal
                    move_dir = 'x'
                    start_pos = (obj.x,  obj.y + obj.height /2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height /2 )
                else: #vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width/2,  obj.y)
                    end_pos = (obj.x + obj.width/2, obj.y + obj.height )
                speed = obj.properties['speed']
                MovingSprite((self.all_sprites,self.collision_sprites), start_pos, end_pos, move_dir, speed)

                


    def run(self,dt):
        self.diplay_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)
        
        
        
		

	
     