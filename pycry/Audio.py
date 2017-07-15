import os
import pygame

_currentMusic = None

class Music:
	
	def __init__(self, path):
		self.path = path
	
	def fadeIn(self, loop, inTransition):
		pass
		
	def fadeOut(self, outTransition):
		pass
		
	def fadeOutAndIn(self,  loop, outTransition, inTransition):
		pass
		
	def fadeOutAndPlay(self, loop, outTransition):
		pass
		
	@staticmethod
	def fadeOutCurrent(outTransition):
		if _currentMusic != None:
			_currentMusic.fadeOut(outTransition)
		
	@staticmethod
	def getCurrent():
		pass
		
	@staticmethod
	def loadFromResource(path):
		return Music(path.replace('/', os.sep))
		
	def play(self, loop):
		global _currentMusic
		pygame.mixer.music.load(self.path)
		pygame.mixer.music.play(-1 if loop else 1)
		_currentMusic = self
		
	@staticmethod
	def stop():
		global _currentMusic
		if _currentMusic != None:
			pygame.mixer.music.stop()
			_currentMusic = None


class Sound:
	def getPan():
		pass
		
	def getResource():
		pass
		
	def getState():
		pass
		
	def getVolume():
		pass
		
	def resume():
		pass
		
	def setPan(value):
		pass
		
	def setVolume(ratio):
		pass
		
	def stop():
		pass

		
class SoundResource:
	def __init__(self, resPath, nativeSound):
		self.resPath = resPath
		self.snd = nativeSound
		self.defaultVolume = 1.0
		
	def getDefaultVolume(self):
		return self.defaultVolume
		
	@staticmethod
	def loadFromFile(path):
		pass
		
	@staticmethod
	def loadFromResource(path):
		rpath = path.replace('/', os.sep)
		snd = pygame.mixer.Sound(rpath)
		return SoundResource(rpath, snd)
		
	def play(self, pan = 0.0):
		self.snd.play()
		# TODO: return Sound
		
	def setDefaultVolume(self, ratio):
		self.defaultVolume = ratio
