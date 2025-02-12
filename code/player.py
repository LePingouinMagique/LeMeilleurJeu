from settings import * 
from timer import Timer


class Player(pygame.sprite.Sprite): 
    def __init__(self,pos,groups,collision_sprites): 
        super().__init__(groups) 
        self.image = pygame.Surface((48,56)) #cration d'uen nouvelle surface 
        self.image.fill('yellow') 
        
        #rects
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        
        #mouv
        self.direction = vector(0,0)
        self.speed = 300 #200
        self.gravity = 1900
        self.jump = False
        self.jump_height = 1000
        self.wall_jump_power = 1.2
        
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
            'wall jump': Timer(270), # durée de la propulsion d'un wall jump
            'time before wall jump':Timer(100),  #temps qu'il faut au personnage pour d'abord glisser sur le mur avant de pouvoir wall jump
            'jump':Timer(200)  # latence entre chaque jump (indépendant de wall juump)
        }
        
        
        #TEST######################
        # Initialisation de la manette
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
    
        
    def input(self):
        self.frottements = False
        keys =  pygame.key.get_pressed()
        input_vector = vector(0,0)
        if not self.timers["wall jump"].active:
            
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                #print("right")
                input_vector.x +=1
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                input_vector.x -=1
                
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x # genre ca met la taille max a 1

            #on vérifie ici si le joueur est collé et glisse contre un mur et appui sur la touche dans le meme sens
            if (self.on_surface['right'] and (keys[pygame.K_RIGHT] or keys[pygame.K_d])) or (self.on_surface['left'] and (keys[pygame.K_LEFT] or keys[pygame.K_q])):
                self.frottements = True

        #jump
        if keys[pygame.K_SPACE] and not self.timers["jump"].active:
            self.timers["jump"].activate()
            self.jump = True

            
    
    def move(self,dt):
        #horizontal
        self.rect.x += self.direction.x * self.speed * dt  # dt => tjr avoir la même vitesse
        self.collision('horizontal')
        if not self.on_surface['floor'] and any((self.on_surface['right'],self.on_surface['left'])) and not self.timers["jump"].active :
            
            if self.arrivée_paroie == 0:
                self.arrivée_paroie =1
                self.timers["time before wall jump"].activate()
            elif self.arrivée_paroie == 1 or self.arrivée_paroie == 2:
                self.arrivée_paroie = 2
                
            self.direction.y = 0
            
            if self.frottements:
                self.rect.y += self.gravity /20 * dt    # touche appuyé meme sens pendant glissade
            else:
                self.rect.y += self.gravity /10 * dt
        else:
            if not self.platform:
                self.arrivée_paroie = 0
                #vertical  # formule bizarre que je comprends pas
                self.direction.y += self.gravity/2*dt
                self.rect.y += self.direction.y*dt
                self.direction.y += self.gravity/2*dt
            else:
                self.direction.y = 0
        self.collision('vertical')
        if self.on_surface['roof']:
            self.direction.y = 20

        if self.jump:
            if self.on_surface["floor"] or self.platform:  #JUMP NORMAL
                #print("z")
                self.direction.y = - self.jump_height
                self.rect.bottom -= 3
                
            elif any((self.on_surface['right'], self.on_surface['left'])) and not self.on_surface["floor"] and not self.timers["time before wall jump"].active:  #WALL JUMP
                print("#"*99)
                self.timers["wall jump"].activate()
                
                self.direction.y = - self.jump_height
                self.direction.x = self.wall_jump_power if self.on_surface['left'] else -self.wall_jump_power
            self.jump = False
        
        
        #print(self.jump)
        # print(self.on_surface['floor'])
               
    def platform_move(self,dt):
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * dt
            
            
    def check_contact(self):
        #for explain :  code\explain\contact_with.png  on crée 3 rectengle et on check les contacts
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + vector(0,self.rect.height /4),(2,self.rect.height /2))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height /4 ) , (2, self.rect.height/2))  #Les deux rectangles sur les cotés du joueur
        roof_rect = pygame.Rect(self.rect.topleft + vector(0,-2),(self.rect.width, 2))
        #drawing colision rectangle 
        pygame.draw.rect(self.display_surface, "red", floor_rect)
        pygame.draw.rect(self.display_surface, "red", right_rect)
        pygame.draw.rect(self.display_surface, "red", left_rect)
        pygame.draw.rect(self.display_surface, "red", roof_rect)
        
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
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':    #horizontal_collision gestion
                    #left collision
                    #print("overlap")
                    
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right: #gauche
                        self.rect.left = sprite.rect.right
                        
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left: #droite
                        self.rect.right = sprite.rect.left
    
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top: #en bas
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom: #en heut
                        self.rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.rect.y +=6
           
                
    def uptate_timer(self):
        for timer in self.timers.values():
            timer.update() #update chaque timer pour le joueur
        
         
    def update(self,dt):
        
        self.old_rect = self.rect.copy()#a faire avant tout pour avoir l'ancienne position du joueur
        #uptate the times
        self.uptate_timer()
        #séxacute a chaque toursde boucle
        self.input()
        self.controller_input()
        #print(self.direction)
        self.move(dt)
        
        self.platform_move(dt)
        #check les contact avecc les trois rectengla dun jouer droite gauche bas
        self.check_contact()

        
    
        #print(self.timers['wall jump'].active)
        #print(self.direction)
        
        #print(   self.timers["time before wall jump"].active   )
        #print(self.arrivée_paroie)
        print(self.platform)
        
        
        
        



        
        
