import pygame
from sprites import AnimatedSprite
from settings import *
from random import randint
from timer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surf = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        # Zoom factor
        zoom = 0.15

        # health
        heart_frames_original = frames['heart']
        self.heart_frames = [
            pygame.transform.scale(i, (int(i.get_width() * zoom), int(i.get_height() * zoom)))
            for i in heart_frames_original
        ]
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 5

        # coins
        self.coins_amount = 0
        self.old_coins_amount = 0
        self.add_coins_amount = 0
        self.coins_timer = Timer(3500)
        self.end_timer = False
        self.pas = True
        self.coin_surf = pygame.transform.scale(
            frames['coin'],
            (int(frames['coin'].get_width() * zoom), int(frames['coin'].get_height() * zoom))
        )

        # calices
        self.calis_surf = pygame.transform.scale(
            frames['calice'],
            (int(frames['calice'].get_width() * zoom), int(frames['calice'].get_height() * zoom))
        )
        self.calis_black_surf = pygame.transform.scale(
            frames['calice_black'],
            (int(frames['calice_black'].get_width() * zoom), int(frames['calice_black'].get_height() * zoom))
        )

        # number of calices collected (default to 0)
        self.calice_count = 0
        self.max_calices = 5  # Change as needed

    def display_text(self):
        # Coin animation text
        if self.coins_timer.active:
            text2_surf = self.font.render("+ " + str(self.add_coins_amount), False, 'white')
            text2_rect = text2_surf.get_frect(topleft=(13, 34)).move(30, 30)
            self.display_surf.blit(text2_surf, text2_rect)
        elif self.end_timer:
            self.coins_amount += 1 if self.pas else 0
            self.pas = not self.pas
            if self.coins_amount == self.old_coins_amount + self.add_coins_amount:
                self.end_timer = False

        # Coin count display
        text_surf = self.font.render(str(self.coins_amount), False, 'white')
        text_rect = text_surf.get_frect(topleft=(13, 34)).move(30, 0)
        self.display_surf.blit(text_surf, text_rect)
        coin_rect = self.coin_surf.get_frect(center=text_rect.bottomleft).move(-22, -20)
        self.display_surf.blit(self.coin_surf, coin_rect)

        # Calices display (top right)
        for i in range(self.max_calices):
            if i < self.calice_count:
                surf = self.calis_surf
            else:
                surf = self.calis_black_surf

            x = self.display_surf.get_width() - (surf.get_width() + 10) * (self.max_calices - i)
            y = 10
            self.display_surf.blit(surf, (x, y))

    def show_coin(self, amount):
        self.coins_timer.activate()
        self.end_timer = True
        self.old_coins_amount = self.coins_amount
        self.add_coins_amount = amount - self.coins_amount

    def create_hearts(self, amount):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(amount):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x, y), self.heart_frames, self.sprites)

    def update(self, dt):
        self.coins_timer.update()
        self.sprites.update(dt)
        self.sprites.draw(self.display_surf)
        self.display_text()

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0

    def update(self, dt):
        if self.active:
            self.animate(dt)
        else:
            if randint(0, 500) == 4:
                self.active = True
