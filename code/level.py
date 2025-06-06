import pygame


from settings import *
#sinon import *
from sprites import Sprite, MovingSprite, Wall, AnimatedSprite, Spike, Item, ParticleEffectSprite
from player import Player
from groups import AllSprites
from enemies import Tooth, Shell, Pearl, Crow
from sound import SoundManager

class Level:
    def __init__(self, tmx_map, level_frames, data, game,name):# prndsen paramètre une carte à l'appelle
        self.game = game
        self.name =name
        self.diplay_surface = pygame.display.get_surface()
        self.data = data
        self.checkpoints = []
        self.sound_manager = SoundManager()
        self.sound_manager.play_music(name)
        #level data
        self.level_width = tmx_map.width*TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        tmx_level_propreties = tmx_map.get_layer_by_name('Data')[0].properties  #bg
        if tmx_level_propreties['bg']:
            bg_tile = level_frames['bg_tiles'][tmx_level_propreties['bg']]
        else:
            bg_tile = None
        
        #groups
        self.all_sprites = AllSprites(width= tmx_map.width,
                                      height= tmx_map.height,
                                      bg_tile= bg_tile,
                                      top_limit= tmx_level_propreties['top_limit'],
                                      clouds = {'large':level_frames["cloud_large"],'small':level_frames['cloud_small']},
                                      horizon_line = tmx_level_propreties['horizon_line'])
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()
        self.pearl_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()

        self.transitions_rects = []

        
        
        #######
        self.setup(tmx_map, level_frames)

        #frames
        self.pearl_surf = level_frames["pearl"]
        self.particle_frames = level_frames['particle']
        
    def setup(self,tmx_map, level_frames):
        for obj in tmx_map.get_layer_by_name('Objects'):  # ex <TiledObject[15]: "player">

            if obj.name == "player":
                
                self.player = Player(
                    pos=(obj.x,obj.y),
                    groups=self.all_sprites, 
                    collision_sprites=self.collision_sprites,
                    frames = level_frames['player'],
                    data = self.data,
                    level_ = self)
                
                
                
            else:
                if obj.name in ('barrel','crate'): #object pas animéeée => one only imâge
                    Sprite((obj.x,obj.y),obj.image, (self.all_sprites, self.collision_sprites))
                else: #objects avec plusieurs images
                    
                    frames = frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    if obj.name == "floor_spike":

                        AnimatedSprite((obj.x, obj.y), frames, (self.all_sprites,self.damage_sprites),reverse=obj.properties['inverted'])
                    else:

                        AnimatedSprite((obj.x,obj.y),
                                       frames,
                                       (self.all_sprites) if obj.name != "saw" else (self.all_sprites,self.damage_sprites),
                                       zoom = obj.properties['zoom'] if "zoom" in obj.properties else 1,
                                       speed_acc = obj.properties['speed_acc'] if "speed_acc" in obj.properties else 1)

            if obj.name == 'flag':
                self.level_finish_rect = pygame.FRect((obj.x,obj.y),(obj.width,obj.height))
            else:
                self.level_finish_rect = False

        #checkpoints
        try:
            for obj in tmx_map.get_layer_by_name('checkpoints'):
                self.checkpoints.append(pygame.FRect((obj.x,obj.y),(obj.width,obj.height)))
                print(self.checkpoints)
        except:
            print("no checkpoints")

                    
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'static':

                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z = Z_LAYERS['bg tiles']+1)
            else:
                if obj.name == 'candle':
                    AnimatedSprite((obj.x, obj.y) + vector(-20,-20), level_frames['candle_light'], self.all_sprites, Z_LAYERS['bg tiles']+2)
                
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites,z = Z_LAYERS['bg tiles'] + 1)
        
        #tiles
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
                        z = Z_LAYERS['bg tiles']-1
                    case _ :
                        z = Z_LAYERS["main"]-1

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
                groups = (self.all_sprites, self.collision_sprites) if obj.properties['platform'] else (self.all_sprites,self.damage_sprites) #self.damage_sprite ))
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

        #hitbox
        if 1 ==1:
            for obj in tmx_map.get_layer_by_name("Objects2"):
                if obj.type == "solid":
                    Wall((obj.x, obj.y), (obj.width, obj.height), (self.collision_sprites))

        
        #enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x,obj.y),level_frames['tooth'],(self.all_sprites,self.damage_sprites,self.tooth_sprites ), self.collision_sprites)
            if obj.name == 'crow':
                Crow((obj.x, obj.y), level_frames['crow'],(self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
                
            if obj.name == 'shell':
                Shell(pos = (obj.x,obj.y),
                      frames=level_frames['shell'],
                      groups = (self.all_sprites,self.collision_sprites),
                      reverse= obj.properties['reverse'],
                      player = self.player,
                      create_pearl = self.create_pearl)


        #items
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name,(obj.x +TILE_SIZE/2,obj.y+ TILE_SIZE/2),level_frames['items'][obj.name],(self.all_sprites,self.item_sprites),self.data,self)

        #transitions
        for obj in tmx_map.get_layer_by_name('Transitions'):
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            transition = (rect,obj.name)
            self.transitions_rects.append(transition)

        #water
        for obj in tmx_map.get_layer_by_name('Water'):
            rows = int(obj.height/ TILE_SIZE)
            cols = int(obj.width/TILE_SIZE)
            for row in range(rows):
                for col in range(cols):
                    x = obj.x+ col*TILE_SIZE
                    y = obj.y+ row*TILE_SIZE
                    if row == 0:
                        AnimatedSprite((x,y),level_frames['water_top'],self.all_sprites, Z_LAYERS['water'])
                    else:
                        Sprite((x,y), level_frames['water_body'],(self.all_sprites,self.collision_sprites), Z_LAYERS['water'])


    def create_pearl(self,pos,direction):
        Pearl(pos, (self.all_sprites, self.damage_sprites, self.pearl_sprites),self.pearl_surf, direction, 150)

    def pearl_collision(self):
        #method is running in the updattes level (not called in pearl or shell)
        for sprite in self.collision_sprites:
            collide_sprite = pygame.sprite.spritecollide(sprite, self.pearl_sprites, True)
            if collide_sprite:

                ParticleEffectSprite((collide_sprite[0].rect.center), self.particle_frames, self.all_sprites)

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                if hasattr(sprite,'tooth'):
                    if sprite.dead == True:
                        pass
                    else:
                        self.player.get_damage()
                else:
                    self.player.get_damage()
                if hasattr(sprite, 'pearl'): #permet de détruire la perle
                    sprite.kill()
                    ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites)

    def checkpoints_check(self):
        for checkpoint in self.checkpoints:

            if checkpoint.colliderect(self.player.hitbox_rect):
                self.player.checkpoint = checkpoint.topleft


 
    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player,self.item_sprites,True)
            if item_sprites:
                item_sprites[0].activate()
                ParticleEffectSprite((item_sprites[0].rect.center),self.particle_frames,self.all_sprites)
                #print(item_sprites[0].item_type)

    def level_transitions_check(self):
        for transition in self.transitions_rects:
            if transition[0].colliderect(self.player.hitbox_rect):
                self.game.change_state(transition[1])
                self.sound_manager.stop_music(self.name)

    def attack_collision(self):
        for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites():
            facing_target = (self.player.rect.centerx < target.rect.centerx and self.player.facing_right) or (self.player.rect.centerx > target.rect.centerx and not self.player.facing_right)
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                target.reverse()

    def check_constraint(self):
        #left right
        if self.player.hitbox_rect.left<=0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right>=self.level_width:
            self.player.hitbox_rect.right = self.level_width

        #bottom border
        if self.player.hitbox_rect.bottom > self.level_bottom:
            self.data.health -=1

        #success
        if self.level_finish_rect:
            if self.player.hitbox_rect.colliderect(self.level_finish_rect):
                print("success")

    def run(self,dt):
        self.diplay_surface.fill('black')
        self.level_transitions_check()
        self.all_sprites.update(dt)
        self.pearl_collision()
        self.hit_collision()
        self.item_collision()
        self.attack_collision()
        self.check_constraint()
        self.checkpoints_check()

        self.all_sprites.draw(self.player.hitbox_rect.center,dt)                                                                                                                                                            
        
        
        
        
		

	
     