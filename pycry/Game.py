import time
import pygame

class GameWindow:
	def __init__(self, title, fps, gameWidth, gameHeight, screenWidth, screenHeight):
		self.title = title
		self.fps = fps + 0.0
		self.width = gameWidth
		self.height = gameHeight
		
		pygame.init()
		self.realScreen = pygame.display.set_mode((screenWidth, screenHeight))
		pygame.display.set_caption(title)
		self.virtualScreen = pygame.Surface((gameWidth, gameHeight))
		self.lastFrame = time.time()
	
	def pumpEvents(self):
		output = []
		for event in pygame.event.get():
			output.append(event)
		
		return output
	
	def clockTick(self):
		pygame.transform.scale(self.virtualScreen, self.realScreen.get_size(), self.realScreen)
		pygame.display.flip()
		now = time.time()
		diff = now - self.lastFrame
		delay = 1 / self.fps - diff
		if delay <= 0:
			delay = 0.001
		time.sleep(delay)
	
		
		