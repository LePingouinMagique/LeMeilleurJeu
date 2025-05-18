import pygame


class SoundManager:
    def __init__(self):
        self.sounds = {
             'hit': pygame.mixer.Sound('audio/hit.wav'),
            'pearl': pygame.mixer.Sound('audio/pearl.wav'),
            'jump': pygame.mixer.Sound('audio/jump.wav'),
            'damage': pygame.mixer.Sound('audio/damage.wav'),
            'coin': pygame.mixer.Sound('audio/coin.wav'),}


        self.musics = {
            'ship2': pygame.mixer.Sound("Mine/musics/ship2.mp3"),
            'parcours1': pygame.mixer.Sound("Mine/musics/parcours1.mp3"),
            'parcours2': pygame.mixer.Sound("Mine/musics/parcours2.ogg"),


        }

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def play_music(self, music_name):
        print(music_name)
        self.musics[music_name].play(loops=-1)

    def stop_music(self, music_name):
        print(music_name)
        self.musics[music_name].stop()
    def start_footsteps(self):
        """Starts playing the footstep sound effect in a loop."""
        if 'footsteps' in self.sounds:
            self.sounds['footsteps'].play(loops=-1)  # Loop indefinitely
        else:
            print("Footstep sound not found!")

    def stop_footsteps(self):
        """Stops the footstep sound effect."""
        if 'footsteps' in self.sounds:
            self.sounds['footsteps'].stop()
        else:
            print("Footstep sound not found!")