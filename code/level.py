from settings import *
from sprites import Sprite, MovingSprite, Wall, AnimatedSprite, Spike
from player import Player
from groups import AllSprites
from enemies import Tooth, Shell

class Level:
    def __init__(self, tmx_map, level_frames):  # prndsen paramètre une carte à l'appelle
        self.diplay_surface = pygame.display.get_surface()
        
        #groups
        self.all_sprites = AllSprites()
        
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()
        
        
        #######
        self.setup(tmx_map, level_frames)
        
    def setup(self,tmx_map, level_frames):
        for obj in tmx_map.get_layer_by_name('Objects'):  # ex <TiledObject[15]: "player">
            if obj.name == "player":
                
                self.player = Player(
                    pos=(obj.x,obj.y),
                    groups=self.all_sprites, 
                    collision_sprites=self.collision_sprites,
                    frames = level_frames['player'])
                
                
                
            else:
                if obj.name in ('barrel','crate'): #object pas animéeée => one only imâge
                    Sprite((obj.x,obj.y),obj.image, (self.all_sprites, self.collision_sprites))
                else: #objects avec plusieurs images
                    
                    frames = frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    AnimatedSprite((obj.x,obj.y),frames,self.all_sprites)
                    
                    
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'static':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z = Z_LAYERS['bg tiles']+1)
            else:
                if obj.name == 'candle':
                    AnimatedSprite((obj.x, obj.y) + vector(-20,-20), level_frames['candle_light'], self.all_sprites, Z_LAYERS['bg tiles']+2)
                
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites,z = Z_LAYERS['bg tiles'] + 1)
        
        
        for layer in ['BG','Terrain','FG','Platforms']:
            #tiles
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles(): # prens les positions x,y et la surface de chaque tuile du calque "Terrain"
                
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)    # sprite avec les quels il y a de la collision !
                #if layer == 'Platforms': groups.append(self.collision_sprites)
                
                match layer:
                    case 'BG':
                        z = Z_LAYERS['bg tiles']
                    case 'FG':
                        z = Z_LAYERS['bg tiles']
                    case _ :
                        z = Z_LAYERS["main"] -1
                Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,groups,z)
                
                
        
        #moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            #1)  Movings platforms
            if obj.name == 'spike':
                Spike(
                    pos = (obj.x+ obj.width/2, obj.y+ obj.height/2),
                    surf = level_frames['spike'],
                    radius = obj.properties['radius'],
                    speed = obj.properties['speed'],
                    start_angle = obj.properties['start_angle'],
                    end_angle = obj.properties['end_angle'],
                    groups= (self.all_sprites,self.damage_sprites)  ##  ))
                )
                
                for radius in range(0, obj.properties['radius'],20):
                    Spike(
                        pos = (obj.x+ obj.width/2, obj.y+ obj.height/2),
                        surf = level_frames['spike_chain'],
                        radius = radius,
                        speed = obj.properties['speed'],
                        start_angle = obj.properties['start_angle'],
                        end_angle = obj.properties['end_angle'],
                        groups= (self.all_sprites),
                        z= Z_LAYERS["bg details"]
                    )
            else:
                frames = level_frames[obj.name]
                #print(frames)
                groups = (self.all_sprites, self.collision_sprites) if obj.properties['platform'] else (self.all_sprites) #self.damage_sprite ))
                if obj.width > obj.height: #horizontal
                    move_dir = 'x'
                    start_pos = (obj.x,  obj.y + obj.height/2 )
                    end_pos = (obj.x + obj.width, obj.y + obj.height /2 )
                else: #vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width/2,  obj.y)
                    end_pos = (obj.x + obj.width/2, obj.y + obj.height )
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])
                
                if obj.name == 'saw':
                    if move_dir == 'x':
                        y = start_pos[1] - level_frames["saw_chain"].get_height()/2
                        left, right = int(start_pos[0]), int(end_pos[0])
                        for x in range(left,right,20):
                            Sprite((x,y),level_frames["saw_chain"],self.all_sprites,z = 2)
                    else:
                        x = start_pos[0] - level_frames['saw_chain'].get_width()/2
                        top,bottom = int(start_pos[1]), int(end_pos[1])
                        for y in range(top,bottom,20):
                            Sprite((x,y),level_frames["saw_chain"],self.all_sprites,z = 2)
                            

        if 1 ==1:
            for obj in tmx_map.get_layer_by_name("Objects2"):
                if obj.type == "solid":
                    Wall((obj.x, obj.y), (obj.width, obj.height), [ self.collision_sprites])

        
        #enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x,obj.y),level_frames['tooth'],(self.all_sprites,self.damage_sprites), self.collision_sprites)
                
            if obj.name == 'shell':
                Shell((obj.x,obj.y),level_frames['shell'],(self.all_sprites,self.collision_sprites),obj.properties['reverse'])



    def run(self,dt):
        self.diplay_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)
        
        
        
        
		

	
     