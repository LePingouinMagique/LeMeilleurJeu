import pygame

from settings import *
from timer import Timer
from os.path import join
from math import sin
from sound import SoundManager

class Player(pygame.sprite.Sprite): 
    def __init__(self,pos,groups,collision_sprites, frames,data,level_):
        #general setup
        super().__init__(groups)
        self.sound_manager = SoundManager()
        self.z = Z_LAYERS['main']
        self.data = data
        self.checkpoint = pos
        self.level_ = level_
        #image
        self.frames, self.frames_index = frames, 0
        self.state , self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frames_index]
        
        #rects
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox_rect = self.rect.inflate(-76,-36)
        self.old_rect = self.hitbox_rect.copy()
        
        #mouv
        self.direction = vector(0,0)
        self.speed = 450 #200
        self.gravity = 1900
        self.jump = False
        self.jump_height = 700
        self.wall_jump_power = 1.0
        self.attacking = False
        self.boost = 1.5
        self.jump_sup = -60

        self.rainbow = [""]
        
        self.arrivée_paroie = 0   #cette variable permet d'utiliser un cooldown (wall jump => un peu de glissade avant) lorsque que lon retouche une paroie (cad avant que  on en touche)
                                    # 0=> pas sur une paroie
                                    # 1=> viens d'arrivée sur une paroie
                                    # 2=> deuxième tour de boucle ou 1<k tour de boucle
        #collision
        self.collision_sprites = collision_sprites #donne tout les autres sprites
        self.on_surface = {'floor':False, 
                           'left':False,
                           'right':False,
                           'roof':False
                           }
        self.platform = None
        
        #display
        self.display_surface = pygame.display.get_surface()
        
        #timer
        self.timers = {
            'wall jump': Timer(190), # durée de la propulsion d'un wall jump
            'time before wall jump':Timer(60),  #temps qu'il faut au personnage pour d'abord glisser sur le mur avant de pouvoir wall jump
            'jump':Timer(200),  # latence entre chaque jump (indépendant de wall juump)
            'attack block': Timer(500),
            'hit': Timer(400),
            'lose_health':Timer(1500),
            'boost':Timer(10000),
            'jump_sup':Timer(120),
            'start_gravity':Timer(1000)
        }
        self.timers['start_gravity'].activate()
        
        
        #TEST######################
        # Initialisation de la manette
        if MANNETTE :
            pygame.joystick.init()
            if pygame.joystick.get_count() > 0:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                print(f"Manette détectée : {self.joystick.get_name()}")
            else:
                self.joystick = None
                print("⚠️ Aucune manette détectée !")
        ##########################

    def controller_input(self):
        """Gestion des entrées manette"""
        if not self.joystick:
            return

        DEADZONE = 0.2

        # Stick droit pour déplacement
        x_axis = self.joystick.get_axis(0)  # Stick droit horizontal

        if abs(x_axis) > DEADZONE:
            self.direction.x = x_axis
        else:
            self.direction.x = 0

        # Bouton B pour sauter (souvent le bouton 1 sur les manettes Switch Pro)
        if self.joystick.get_button(1) and not self.timers["jump"].active:
            self.timers["jump"].activate()
            self.jump = True
        elif self.joystick.get_button(0):
            self.rect.x , self.rect.y = 652 , 330
            self.direction.y = 0

    
        
    def input(self):
        self.frottements = False
        keys =  pygame.key.get_pressed()
        input_vector = vector(0,0)
        if not self.timers["wall jump"].active:
            
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                #print("right")
                input_vector.x +=1
                self.facing_right = True
                
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                input_vector.x -=1
                self.facing_right = False

            if keys[pygame.K_m]:
                self.attack()
            
                
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x # genre ca met la taille max a 1

            #on vérifie ici si le joueur est collé et glisse contre un mur et appui sur la touche dans le meme sens
            if (self.on_surface['right'] and (keys[pygame.K_RIGHT] or keys[pygame.K_d])) or (self.on_surface['left'] and (keys[pygame.K_LEFT] or keys[pygame.K_q])):
                self.frottements = True

        #jump
        if keys[pygame.K_SPACE] and not self.timers["jump"].active:
            self.timers["jump"].activate()
            self.jump = True
        if keys[pygame.K_SPACE] and self.timers['jump_sup'].active:
            self.direction.y += self.jump_sup
        if keys[pygame.K_g]:
            self.hitbox_rect.x , self.hitbox_rect.y = 652 , 330
            self.direction.y = 0
           
    def attack(self):
        if not self.timers['attack block'].active:
            self.attacking = True
            self.frames_index = 0
            self.timers['attack block'].activate()
            
    def move(self,dt):
        #horizontal
        self.hitbox_rect.x += self.direction.x * self.speed * dt  # dt => tjr avoir la même vitesse
        self.collision('horizontal')
        if not self.on_surface['floor'] and any((self.on_surface['right'],self.on_surface['left'])) and not self.timers["jump"].active :
            
            if self.arrivée_paroie == 0:
                self.arrivée_paroie =1
                self.timers["time before wall jump"].activate()
            elif self.arrivée_paroie == 1 or self.arrivée_paroie == 2:
                self.arrivée_paroie = 2
                
            self.direction.y = 0
            
            if self.frottements:
                self.hitbox_rect.y += self.gravity /20 * dt    # touche appuyé meme sens pendant glissade
            else:
                self.hitbox_rect.y += self.gravity /10 * dt
        else:
            if not self.platform:
                self.arrivée_paroie = 0
                #vertical  # formule bizarre que je comprends pas
                if not self.timers['start_gravity'].active:
                    self.direction.y += self.gravity/2*dt
                    self.hitbox_rect.y += self.direction.y*dt
                    self.direction.y += self.gravity/2*dt
            else:
                self.direction.y = 0
        self.collision('vertical')
        if self.on_surface['roof']:
            self.direction.y = 20

        if self.jump:
            if self.on_surface["floor"] or self.platform:  #JUMP NORMAL
                #print("z")
                self.timers['jump_sup'].activate()

                self.direction.y = - self.jump_height
                self.sound_manager.play_sound('jump')
                self.hitbox_rect.bottom -= 3
            
                
            elif any((self.on_surface['right'], self.on_surface['left'])) and not self.on_surface["floor"] and not self.timers["time before wall jump"].active:  #WALL JUMP
                #print("#"*99)
                self.timers["wall jump"].activate()
                self.sound_manager.play_sound('jump')
                
                self.direction.y = - self.jump_height
                self.direction.x = self.wall_jump_power if self.on_surface['left'] else -self.wall_jump_power
            self.jump = False
        
        self.rect.center = self.hitbox_rect.center
        #print(self.jump)
        # print(self.on_surface['floor'])
             
               
    def platform_move(self,dt):
        if self.platform:
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * dt
            self.rect.y += 1
            
            
    def check_contact(self):
        #for explain :  code\explain\contact_with.png  on crée 3 rectengle et on check les contacts
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0,self.hitbox_rect.height /4),(2,self.hitbox_rect.height /2))
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height /4 ) , (2, self.hitbox_rect.height/2))  #Les deux rectangles sur les cotés du joueur
        roof_rect = pygame.Rect(self.hitbox_rect.topleft + vector(0,-2),(self.hitbox_rect.width, 2))
        #drawing colision rectangle 
        # pygame.draw.rect(self.display_surface, "red", floor_rect)
        # pygame.draw.rect(self.display_surface, "red", right_rect)
        # pygame.draw.rect(self.display_surface, "red", left_rect)
        # pygame.draw.rect(self.display_surface, "red", roof_rect)
        
        collide_rects_list = [sprite.rect for sprite in self.collision_sprites]
        
        #check collision
        self.on_surface['floor'] =True if floor_rect.collidelist(collide_rects_list)  >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects_list) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects_list)   >= 0 else False
        self.on_surface['roof'] = True if roof_rect.collidelist(collide_rects_list)   >= 0 else False
        

        #print(self.on_surface)
        self.platform = None
        for sprite in [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
        
        
    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                #print(sprite)
                if axis == 'horizontal':    #horizontal_collision gestion
                    #left collision
                    #print("overlap")
                    
                    if self.hitbox_rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right: #gauche
                        self.hitbox_rect.left = sprite.rect.right
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.x +=4
                        
                    if self.hitbox_rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left: #droite
                        self.hitbox_rect.right = sprite.rect.left
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.x -=4
                else:
                    if self.hitbox_rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top: #en bas
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.direction.y = 0
                    if self.hitbox_rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom: #en heut
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.hitbox_rect.y +=6
           
                
    def uptate_timer(self):
        for timer in self.timers.values():
            timer.update() #update chaque timer pour le joueur

    def boost_with_item(self):
        if not self.timers['boost'].active:
            self.timers['boost'].activate()
            self.speed *= self.boost
            self.jump_height *= self.boost
            
         
    def animate(self,dt):
        self.frames_index += ANIMATION_SPEED * dt
        if self.state == 'attack' and self.frames_index >= len(self.frames[self.state]):
            self.state = 'idle'
        self.image = self.frames[self.state][int(self.frames_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image,True,False)
    
        if self.attacking and self.frames_index >= len(self.frames[self.state]):
            self.attacking = False


    def get_state(self):
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'attack'
            else:
                self.state = 'idle' if self.direction.x == 0 else 'run'
        else:
            if self.attacking:
                self.state = 'air_attack'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state = 'wall'
                else:
                    self.state = 'jump' if self.direction.y < 0 else 'fall'

    def get_damage(self):
        if not self.timers['hit'].active and not self.timers['lose_health'].active:
            self.sound_manager.play_sound('damage')
            self.data.health -= 1
            self.timers['lose_health'].activate()
            self.timers['hit'].activate()

    def check_death(self):
        if self.data.health <= 0:
            self.sound_manager.play_sound('die')
            self.rect = self.image.get_frect(topleft=self.checkpoint)
            self.hitbox_rect = self.rect.inflate(-76,-36)
            self.data.health = self.data.max_health

    def flicker(self):
        if self.timers['hit'].active and sin(pygame.time.get_ticks() / 18)>=0: #pour que ça clignote
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf
    def rainbow(self): #genre &toile mariokart

        '''white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf'''
             
    def update(self,dt):
        
        if not self.timers['boost'].active :
            self.speed = 450 #200
            self.jump_height = 700
        self.check_death()
        self.old_rect = self.hitbox_rect.copy()#a faire avant tout pour avoir l'ancienne position du joueur
        #uptate the times
        self.uptate_timer()
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 = clic gauche
                    self.attack()
        #séxacute a chaque toursde boucle
        self.input()
        if MANNETTE:
            self.controller_input()
        
        #print(self.direction)
        self.move(dt)

        
        self.platform_move(dt)
        #check les contact avecc les trois rectengla dun jouer droite gauche bas
        self.check_contact()

        self.get_state()
        self.animate(dt)
        self.flicker()
    
        #print(self.timers['wall jump'].active)
        #print(self.direction)
        
        #print(   self.timers["time before wall jump"].active   )
        #print(self.arrivée_paroie)
        
        
        
        
        



        
        
