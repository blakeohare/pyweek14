import pygame
import os

def _canonicalizePath(path):
	path = path.replace('\\', '/').replace('/', os.sep)
	if path[:1] == os.sep:
		return path[1:]
	return path
	
class ImageSheet:
	def __init__(self):
		self._imageCache = {}
	
	@staticmethod
	def loadFromResources(idOrIds):
		# Dummy implementation
		return ImageSheet()
		
	@staticmethod
	def loadFromResourcesAsync(idOrIds):
		return loadFromResources(idOrIds)
	
	def isDone(self):
		return True
	
	def getProgres(self):
		return 1.0
	
	def getImage(self, path):
		img = self._imageCache.get(path)
		if img == None:
			pygameImage = pygame.image.load(_canonicalizePath(path))
			width, height = pygameImage.get_size()
			img = ImageResource(width, height, False)
			img.image = pygameImage
			self._imageCache[path] = img
		return img

class ImageResource:
	
	def __init__(self, width, height, _initAsEmpty = True):
		self.width = width
		self.height = height
		self.image = None
		if _initAsEmpty:
			self.image = pygame.Surface((width, height), pygame.SRCALPHA)
