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

	def drawWithAlpha(self, x, y, alpha):
		if alpha < 1: return
		key = self.width * 100000 + self.height
		temp = _tempSurfStore.get(key)
		if temp == None:
			temp = pygame.Surface((self.width, self.height)).convert()
			_tempSurfStore[key] = temp
		temp.blit(_screen, (-x, -y))
		temp.blit(self.pgImage, (0, 0))
		temp.set_alpha(alpha)
		_screen.blit(temp, (x, y))
		
		
	def scale(self, newWidth, newHeight):
		img = pygame.transform.scale(self.pgImage, (newWidth, newHeight))
		output = GraphicsTexture(self.image)
		output.pgImage = img
		output.width = newWidth
		output.height = newHeight
		return output
	
	def flip(self, flipHorizontal, flipVertical):
		output = GraphicTexture(self.image)
		output.pgImage = pygame.transform.flip(self.pgImage, flipHorizontal, flipVertical)
		output.width = self.width
		output.height = self.height
		return output
		
_tempSurfStore = {}
		
class Draw:
	
	@staticmethod
	def rectangle(x, y, width, height, r, g, b, a = 255):
		if height == 1 or width == 1:
			return Draw.line(x, y, x + width - 1, y + height - 1, 1, r, g, b, a)
		
		if a >= 255:
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
		if a >= 255:
			pygameDrawLine(_screen, (r, g, b), (x1, y1), (x2, y2), width)
		else:
			raise Exception("Not implemented: draw line with alpha")

	@staticmethod
	def triangle(x1, y1, x2, y2, x3, y3, r, g, b, a = 255):
		if a >= 255:
			pygame.draw.polygon(_screen, (r, g, b), [(x1, y1), (x2, y2), (x3, y3)])
		else:
			raise Exception("Not implemented: draw triangle with alpha")

	@staticmethod
	def fill(r, g, b):
		_screen.fill((r, g, b))
