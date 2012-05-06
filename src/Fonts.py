_fonts = {}
def get_font(size):
	global _fonts
	key = 'f' + str(size)
	font = _fonts.get(key)
	if font == None:
		font = pygame.font.SysFont(pygame.font.get_default_font(), size)
		_fonts[key] = font
	return font

_text = {}
def get_text(text, size, color):
	global _text
	key = str(size) + "," + str(color) + "|" + text
	image = _text.get(key)
	if image == None:
		font = get_font(size)
		image = font.render(text, True, color)
		_text[key] = image
	return image