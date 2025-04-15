from settings import *
from random import choice
from timer import Timer


class Tooth(pygame.sprite.Sprite):
    def __init__(self,pos,frames,groups,collision_sprite):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.z = Z_LAYERS["main"]
        
        self.direction = choice((-1,1))
        self.collision_rects = [sprite.rect for sprite in collision_sprite]
        self.speed = 120
        
    def update(self,dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))] if self.direction >=0 else pygame.transform.flip(self.frames[int(self.frame_index % len(self.frames))],True,False)
        #move
        
        self.rect.x += self.speed * self.direction * dt
        
        floor_rect_right = pygame.FRect(self.rect.bottomright,(1,1))
        floor_rect_left= pygame.FRect(self.rect.bottomleft,(-1,1))
        right_rect = pygame.FRect(self.rect.topright,(2,-self.rect.height))
        left_rect = pygame.FRect(self.rect.topleft,(-2,-self.rect.height))
        
        
        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction >0:
            self.direction = -1
        elif floor_rect_left.collidelist(self.collision_rects) <0 and self.direction <0:
            self.direction = 1
        elif right_rect.collidelist(self.collision_rects) >0 and self.direction>0:
            self.direction = -1
        elif left_rect.collidelist(self.collision_rects) >0 and self.direction<0:
            self.direction = 1
            
            
class Shell(pygame.sprite.Sprite):
    def __init__(self,pos,frames,groups,reverse, player):
        super().__init__(groups)
        if reverse:
            #flip all frames in frames
            self.frames = {}
            for key, surfs in frames.items():
                self.frames[key] = [pygame.transform.flip(surf,True,False) for surf in surfs]
            self.bullet_direction = -1
            
        else:
            self.frames = frames
            self.bullet_direction = 1
        self.player = player
        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        self.shoot_timer = Timer(3000)
        
    def state_management(self):
        player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = shell_pos.distance_to(player_pos)<500
        player_front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x
        player_level = abs(shell_pos.y - player_pos.y) <30
        if player_near and player_front and player_level and not self.shoot_timer.active:
            self.state = "fire"
            self.frame_index = 0
            self.shoot_timer.activate()
    def update(self,dt):
        self.shoot_timer.update()
        self.state_management()
        
        #animation/attack
        self.frame_index += ANIMATION_SPEED  * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]
            
    
        
            