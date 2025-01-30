from settings import * 
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
        self.speed = 650 #200
        self.gravity = 1600
        self.jump = False
        self.jump_height = 900
        
        #collision
        self.collision_sprites = collision_sprites #donne tout les autres sprites
        self.on_surface = {'floor':False, 
                           'left':False,
                           'right':False
                           }
        
        #display
        self.display_surface = pygame.display.get_surface()
        
    def input(self):
        keys =  pygame.key.get_pressed()
        input_vector = vector(0,0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            #print("right")
            input_vector.x +=1
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            input_vector.x -=1
            
        self.direction.x = input_vector.normalize().x if input_vector.length() > 0 else input_vector.x # genre ca met la taille max a 1
        
        #jump
        if keys[pygame.K_SPACE]:
            
            self.jump = True
            
    
    def move(self,dt):
        #horizontal
        self.rect.x += self.direction.x * self.speed * dt # dt => tjr avoir la même vitesse
        self.collision('horizontal')
        
        if not self.on_surface['floor'] and any((self.on_surface['right'],self.on_surface['left'])):
            self.direction.y = 0
            self.rect.y += self.gravity /10 * dt
        else:
            #vertical  # formule bizarre que je comprends pas
            self.direction.y += self.gravity/2*dt
            self.rect.y += self.direction.y*dt
            self.direction.y += self.gravity/2*dt
        self.collision('vertical')
            
        if self.jump:
            print(self.on_surface['right'])
            if self.on_surface["floor"]:
                #print("z")
                self.direction.y = - self.jump_height
            elif any((self.on_surface['right'], self.on_surface['left'])):
                self.rect.x += 2 if self.on_surface['left'] else -2
                self.direction.y = - self.jump_height//1.25
                
                
            self.jump = False 
        
        
        #print(self.jump)
        # print(self.on_surface['floor'])
        
        
            
            
    def check_contact(self):
        #for explain :  code\explain\contact_with.png  on crée 3 rectengle et on check les contacts
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + vector(0,self.rect.height /4),(2,self.rect.height /2))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height /4 ) , (2, self.rect.height/2))  #Les deux rectangles sur les cotés du joueur
        
        #drawing colision rectangle 
        pygame.draw.rect(self.display_surface, "red", floor_rect)
        pygame.draw.rect(self.display_surface, "red", right_rect)
        pygame.draw.rect(self.display_surface, "red", left_rect)
        
        collide_rects_list = [sprite.rect for sprite in self.collision_sprites]
        
        #check collision
        self.on_surface['floor'] =True if floor_rect.collidelist(collide_rects_list)  >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects_list) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects_list)   >= 0 else False
        self.on_surface['roof'] = True if left_rect.collidelist(collide_rects_list)   >= 0 else False
        

        #print(self.on_surface)
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
                
    def update(self,dt):
        
        self.old_rect = self.rect.copy()#a faire avant tout pour avoir l'ancienne position du joueur
        
        #check les contact avecc les trois rectengla dun jouer droite gauche bas
        self.check_contact()

        #print(self.direction)
        self.move(dt)
        
        #séxacute a chaque toursde boucle
        self.input()
        
        
        
        
        
