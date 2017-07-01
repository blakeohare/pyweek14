import pygame

_screen = None
def addScreenRef(screen):
	global _screen
	_screen = screen

pygameDrawRect = pygame.draw.rect
pygameDrawLine = pygame.draw.line

class GraphicsTexture:
	def __init__(self, image):
		self.image = image
		self.pgImage = image.image
		self.width = image.width
		self.height = image.height
		
	@staticmethod
	def load(imageResource):
		return GraphicsTexture(imageResource)

	def draw(self, x, y):
		_screen.blit(self.pgImage, (x, y))

_tempSurfStore = {}
		
class Draw:
	
	@staticmethod
	def rectangle(x, y, width, height, r, g, b, a = 255):
		if height == 1 or width == 1:
			return Draw.line(x, y, x + width - 1, y + height - 1, 1, r, g, b, a)
		
		if a == 255:
			pygameDrawRect(_screen, (r, g, b), pygame.Rect(x, y, width, height))
		else:
			key = width * 100000 + height
			surf = _tempSurfStore.get(key)
			if surf == None:
				surf = pygame.Surface((width, height)).convert()
				_tempSurfStore[key] = surf
			surf.fill((r, g, b))
			surf.set_alpha(a)
			_screen.blit(surf, (x, y))
	
	@staticmethod
	def line(x1, y1, x2, y2, width, r, g, b, a = 255):
		if a == 255:
			pygameDrawLine(_screen, (r, g, b), (x1, y1), (x2, y2), width)
		else:
			raise Exception("Not implemented: draw line with alpha")

	@staticmethod
	def fill(r, g, b):
		_screen.fill((r, g, b))
