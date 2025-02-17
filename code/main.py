from settings import * 
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption(TITLE)

		self.clock = pygame.time.Clock()

		self.tmx_map = {0:load_pygame(join('data','levels','omni2.tmx'))} #liste qui charge toute les cartes "join('..')"
		self.import_assets()
		self.current_stage = Level(self.tmx_map[0],self.level_frames)
		
		
		# print(self.tmx_map)
		#bg
  
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
			'player': import_sub_folders('graphics','player')
		}
		print(self.level_frames["player"])

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
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()