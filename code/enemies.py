from numpy.array_api import vecdot
import pygame

from settings import *
from random import choice,randint
from timer import Timer
from math import sin



class Tooth(pygame.sprite.Sprite):
    def __init__(self,pos,frames,groups,collision_sprite):
        super().__init__(groups)
        self.tooth = True
        self.health = 2
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.z = Z_LAYERS["main"]
        
        self.direction = choice((-1,1))
        self.collision_rects = [sprite.rect for sprite in collision_sprite]
        self.speed = randint(100,300)
        self.dead = False

        self.hit_Timer = Timer(200)
        self.lose_health = Timer(800)
        self.death_timer = Timer(1000)

    def reverse(self):
        #quand il se prend un coup
        if not self.hit_Timer.active and not self.lose_health.active:
            self.direction *= -1
            self.health -=1
            self.hit_Timer.activate()
            self.lose_health.activate()
    def flicker(self):
        if self.hit_Timer.active and sin(pygame.time.get_ticks() / 18)>=0: #pour que ça clignote
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf
    def death(self):
        white_mask = pygame.mask.from_surface(self.image)

        # Crée une surface noire avec la forme du masque
        black_surf = white_mask.to_surface(setcolor=(1, 0, 0),
                                           unsetcolor=(0, 0, 0, 0))  # Noir visible, fond transparent

        black_surf.set_colorkey((0, 0, 0, 0))  # Active la transparence du fond
        self.image = black_surf

    def update(self,dt):
        self.hit_Timer.update()
        self.lose_health.update()
        self.death_timer.update()




        if not self.dead:
            self.frame_index += ANIMATION_SPEED * dt
            self.image = self.frames[int(self.frame_index % len(self.frames))] if self.direction >=0 else pygame.transform.flip(self.frames[int(self.frame_index % len(self.frames))],True,False)
        else:
            self.image = pygame.transform.scale(self.image,(self.image.width*0.99,self.image.height*0.99))
        #move
        if self.health <=0:
            self.death()
            if not self.death_timer.active:
                print("hello")
                if not self.dead:
                    self.death_timer.activate()
                    self.dead = True
                else:

                    self.kill()

        if not self.dead:
            self.rect.x += self.speed * self.direction * dt
        if not self.dead:
            self.flicker()
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


class Crow(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprite):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames['walk'][self.frame_index]
        self.rect = self.image.get_frect(topleft=pos)
        mask = pygame.mask.from_surface(frames['walk'][0])
        bbox = mask.get_bounding_rects()[0]  # Renvoie une liste, on prend le premier

        # Découpe l'image à la taille du sprite réel
        cropped_image = frames['walk'][0].subsurface(bbox).copy()

        # Remplace l'image et le rect par la version "propre"
        #self.image = cropped_image
        self.rect = frames['walk'][0].get_rect(topleft=(self.rect.left + bbox.x, self.rect.top + bbox.y))
        self.tooth = True
        self.health = 2


        self.z = Z_LAYERS["main"]

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprite]
        self.speed = randint(100, 300)
        self.dead = False

        self.hit_Timer = Timer(200)
        self.lose_health = Timer(800)
        self.death_timer = Timer(1000)

    def reverse(self):
        # quand il se prend un coup
        if not self.hit_Timer.active and not self.lose_health.active:
            self.direction *= -1
            self.health -= 1
            self.hit_Timer.activate()
            self.lose_health.activate()

    def flicker(self):
        if self.hit_Timer.active and sin(pygame.time.get_ticks() / 18) >= 0:  # pour que ça clignote
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf

    def death(self):
        white_mask = pygame.mask.from_surface(self.image)

        # Crée une surface noire avec la forme du masque
        black_surf = white_mask.to_surface(setcolor=(1, 0, 0),
                                           unsetcolor=(0, 0, 0, 0))  # Noir visible, fond transparent

        black_surf.set_colorkey((0, 0, 0, 0))  # Active la transparence du fond
        self.image = black_surf

    def update(self, dt):
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), self.rect, 1)
        self.hit_Timer.update()
        self.lose_health.update()
        self.death_timer.update()

        if not self.dead:
            self.frame_index += ANIMATION_SPEED * dt
            self.image = self.frames['walk'][
                int(self.frame_index % len(self.frames['walk']))] if self.direction >= 0 else pygame.transform.flip(
                self.frames['walk'][int(self.frame_index % len(self.frames['walk']))], True, False)
        else:
            self.image = pygame.transform.scale(self.image, (self.image.width * 0.99, self.image.height * 0.99))
        # move
        if self.health <= 0:
            self.death()
            if not self.death_timer.active:
                print("hello")
                if not self.dead:
                    self.death_timer.activate()
                    self.dead = True
                else:

                    self.kill()

        if not self.dead:
            self.rect.x += self.speed * self.direction * dt
        if not self.dead:
            self.flicker()
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))
        right_rect = pygame.FRect(self.rect.topright, (2, -self.rect.height))
        left_rect = pygame.FRect(self.rect.topleft, (-2, -self.rect.height))

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0:
            self.direction = -1
        elif floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0:
            self.direction = 1
        elif right_rect.collidelist(self.collision_rects) > 0 and self.direction > 0:
            self.direction = -1
        elif left_rect.collidelist(self.collision_rects) > 0 and self.direction < 0:
            self.direction = 1


class Shell(pygame.sprite.Sprite):
    def __init__(self,pos,frames,groups,reverse, player, create_pearl):
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
        self.has_fired = False
        self.create_pearl = create_pearl

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
            
            #fire
            if self.state == 'fire' and int(self.frame_index) == 3 and not self.has_fired:
                print("shooot")
                self.create_pearl(self.rect.center, self.bullet_direction)
                self.has_fired = True
            
        else:
            self.frame_index = 0
            if self.state == 'fire':
                self.state = 'idle'
                self.has_fired = False
            
    
class Pearl(pygame.sprite.Sprite):
    def __init__(self,pos,groups,surf,direction,speed):
        self.pearl = True
        super().__init__(groups)
        self.direction = direction
        self.image = surf
        self.rect = self.image.get_frect(center = pos + vector(50 * direction, 0))
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']
        self.timers = {'lifetime': Timer(7000), "reverse": Timer(250)}
        self.timers['lifetime'].activate()

        self.speed = 100

    def reverse(self):
        if not self.timers['reverse'].active:
            self.timers['reverse'].activate()
            self.direction *= -1

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()
        self.rect.x += self.speed*dt*self.direction

        if not self.timers['lifetime'].active:
            self.kill()


class Woolf(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites, frames):
        super().__init__(groups)
        self.frames = frames
