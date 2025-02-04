from settings import * 
from level import Level

from pytmx.util_pygame import load_pygame
from os.path import join

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption(TITLE)

		self.clock = pygame.time.Clock()

		self.tmx_map = {0:load_pygame(join('..','data','levels','omni.tmx'))} #liste qui charge toute les cartes
		self.current_stage = Level(self.tmx_map[0])
		# print(self.tmx_map)
		#bg

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