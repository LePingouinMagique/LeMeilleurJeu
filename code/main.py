import pygame

from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from debug import debug
from ui import UI

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption(TITLE)
		self.import_assets()
		self.clock = pygame.time.Clock()

		self.ui = UI(self.font,self.ui_frames)
		self.data = Data(self.ui)
		self.tmx_map = {
						"omni2":load_pygame(join('data','levels','parcours2.tmx'))} #liste qui charge toute les cartes "join('..')"
		#"ship2":load_pygame(join('data','levels','ship2.tmx')),
		self.current_stage = Level(self.tmx_map["omni2"],self.level_frames,self.data,self)
		
		
		# print(self.tmx_map)
		#bg
	def change_state(self, name):
		if name not in self.tmx_map:
			if len(self.tmx_map) >= MAX_CACHED_MAPS:
				self.tmx_map.pop(next(iter(self.tmx_map)))  # supprime la plus ancienne
			self.tmx_map[name] = load_pygame(join('data', 'levels', f'{name}.tmx'))

		self.current_stage = Level(self.tmx_map[name], self.level_frames, self.data, self)
  
	def import_assets(self):
		self.level_frames = {
			'flag': import_folder('graphics','level','flag'),
			'saw' : import_folder('graphics','enemies','saw','animation'),
			'floor_spike': import_folder('graphics','enemies','floor_spikes'),
			'palms': import_sub_folders('graphics','level','palms'),
			'candle': import_folder('graphics','level','candle'),
			'window':import_folder('graphics','level','window'),
   			'big_chains':import_folder('graphics','level','big_chains'),
			'small_chains':import_folder('graphics','level','small_chains'),
   			'candle_light':import_folder('graphics','level','candle light'),
			'player': import_sub_folders('graphics','player'),
			'saw':import_folder('graphics','enemies','saw','animation'),
			'saw_chain':import_image("graphics","enemies","saw","saw_chain"),
			'helicopter':import_folder('graphics','level','helicopter'),
			'boat':import_folder('graphics','objects','boat'),
			'spike': import_image("graphics","enemies",'spike_ball','Spiked Ball'),
   			'spike_chain': import_image("graphics","enemies",'spike_ball','spiked_chain'),
			'tooth':import_folder('graphics','enemies','tooth','run'),
			'shell':import_sub_folders('graphics','enemies','shell'),
			'pearl': import_image('graphics','enemies','bullets','pearl'),
			'items': import_sub_folders('graphics','items'),
			'particle': import_folder('graphics','effects','particle'),
			'water_top':import_folder('graphics','level','water','top'),
			'water_body': import_image('graphics', 'level', 'water', 'body'),
			'bg_tiles': import_folder_dict('graphics',"level","bg","tiles"),
			'cloud_small':import_folder('graphics','level','clouds',"small"),
			'cloud_large': import_image('graphics', 'level', 'clouds', "large_cloud"),
			'wolf':import_sub_folders('graphics','enemies','wolf'),
			'crow': import_sub_folders('graphics', 'enemies', 'crow')
		}

		self.font = pygame.font.Font(join('graphics','ui','runescape_uf.ttf'),40)
		self.ui_frames = {
			'heart' : import_folder('graphics','ui','heart'),
			'coin':import_image('graphics','ui','coin')
		}
	def run(self):
		while True:
			dt = self.clock.tick(MAX_FPS) / 1000  #delta time en seconde permet e toujours avoir la même vitesse selon fps meme lower (gernre ça calcul fps + time execution)
			# print(dt)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_KP_0 or event.key == pygame.K_0 :
						pygame.quit()
						sys.exit()

			self.current_stage.run(dt)
			self.ui.update(dt)
			#debug("health : "+ str(self.data.health) + '  coins : ' + str(self.data.coins))

			pygame.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()