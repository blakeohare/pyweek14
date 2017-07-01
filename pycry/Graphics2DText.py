
import random
import os
import pygame
import time

class FontStyle_: pass
FontStyle = FontStyle_()
FontStyle.NORMAL = 0
FontStyle.BOLD = 1
FontStyle.ITALIC = 2
FontStyle.BOLD_ITALIC = FontStyle.BOLD | FontStyle.ITALIC

_PRIVATE_CONSTRUCTOR_ENFORCER = int(random.random() * (10 ** 9))

_fontInstances = {}
_verifiedSystemFonts = {}
_verifiedDiskFonts = {}

def canonicalize_system_font_name_for_pygame(name):
	output = []
	a = ord('a')
	z = ord('z')
	for letter in name.lower():
		code = ord(letter)
		if code >= a and code <= z:
			output.append(letter)
	return ''.join(output)

# PyGame fonts are based on the font PLUS the size and style
class FontResource:
	
	# private constructor, use static factory methods instead
	def __init__(self, path, sysName, style, private):
		if private != _PRIVATE_CONSTRUCTOR_ENFORCER: raise Exception("This constructor is private")
		self.isFile = path != None
		self.isSystem = sysName != None
		self.path = path
		self.sysName = sysName
		self.style = style
		
		if self.isFile:
			self.path = path.replace('\\', '/').replace('/', os.sep)
			if not os.path.exists(path):
				raise Exception("Font does not exist: " + self.path)
			if not _verifiedDiskFonts.get(self.path, False):
				try:
					pygame.font.Font(self.path, 8)
				except:
					raise Exception("File is not a font: " + self.path)
		else:
			if not FontResource.isSystemFontAvailable(self.sysName):
				raise Exception("System font not available: " + self.sysName)
	
	@staticmethod
	def isSystemFontAvailable(name):
		if _verifiedSystemFonts.get(name, False): return True
		
		if len(_verifiedSystemFonts) == 0:
			for fontName in pygame.font.get_fonts():
				_verifiedSystemFonts[fontName] = True
		
		canonical = canonicalize_system_font_name_for_pygame(name)
		if _verifiedSystemFonts.get(canonical, False):
			_verifiedSystemFonts[name] = True
			_verifiedSystemFonts[canonical] = True
			return True
		
		return False
	
	@staticmethod
	def fromPath(path, style = 0):
		return FontResource(path, None, style, _PRIVATE_CONSTRUCTOR_ENFORCER)
	
	@staticmethod
	def fromResource(path, style = 0):
		return FontResource(path, None, style, _PRIVATE_CONSTRUCTOR_ENFORCER)
	
	@staticmethod
	def fromSystem(name, style = 0):
		return FontResource(None, name, style, _PRIVATE_CONSTRUCTOR_ENFORCER)
	
	def getRenderer(self, size, r, g, b):
		# PyGame has its own definition of what font size means, so I will likely
		# have to add my own scale factor or size mapping.
		return FontRenderer(self, size, r, g, b)

_pygame_font_cache = {}

g2d_texture_constructor = None

_text_cache_1 = {}
_text_cache_2 = {}
_text_cache_staleness = [0, 0]

class FontRenderer:
	def __init__(self, fontResource, size, r, g, b):
		self.key = '|'.join(map(str, [fontResource.style, int(size), r, g, b, fontResource.path, fontResource.sysName]))
		font = _pygame_font_cache.get(self.key)
		if font == None:
			bold = (fontResource.style & FontStyle.BOLD) != 0
			italic = (fontResource.style & FontStyle.ITALIC) != 0
			if fontResource.isSystem:
				font = pygame.font.SysFont(fontResource.sysName, size, bold, italic)
			else:
				font = pygame.font.Font(fontResource.path, size)
				if bold: font.set_bold(True)
				if italic: font.set_italic(True)
			_pygame_font_cache[self.key] = font
		self.font = font
		self.color = (r, g, b)
	
	def render(self, text):
	
		# Every 30 accesses, check to see if the two layer cache hasn't been demoted for more than 10 seconds
		_text_cache_staleness[1] += 1
		if _text_cache_staleness[1] % 30 == 0:
			staleness = _text_cache_staleness[0]
			now = time.time()
			if now - staleness > 10:
				_demote_caches()
		
		pygame_image = self.font.render(text, True, self.color)
		key = self.key + '|' + text
		texture = _text_cache_1.get(key)
		if texture != None: return texture
		texture = _text_cache_2.get(key)
		if texture != None:
			_text_cache_1[key] = texture
			return texture
		texture = TextSurface(pygame_image)
		_text_cache_1[key] = texture
		return texture

def _demote_caches():
	global _text_cache_1
	global _text_cache_2
	_text_cache_2 = _text_cache_1
	_text_cache_1 = {}
	_text_cache_staleness[0] = time.time()

class TextSurface:
	def __init__(self, pgImage):
		self.pgImage = pgImage
		self.width, self.height = pgImage.get_size()
		self.graphicsTexture = g2d_texture_constructor(pgImage)
	
	def draw(self, x, y):
		self.graphicsTexture.draw(x, y)

	def drawWithAlpha(self, x, y, alpha):
		self.graphicsTexture.drawWithAlpha(x, y, alpha)
