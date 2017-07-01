_fonts = {}
def get_font(size):
	global _fonts
	key = 'f' + str(size)
	font = _fonts.get(key)
	if font == None:
		font = pygame.font.SysFont(pygame.font.get_default_font(), size)
		_fonts[key] = font
	return font

_COLORS_TO_COMPONENTS = {
	'red': (255, 0, 0),
	'white': (255, 255, 255),
	'black': (0, 0, 0),
}

_text = {}
def get_text(text, size, color):
	global _text
	key = str(size) + "," + str(color) + "|" + text
	texture = _text.get(key)
	if texture == None:
		font = get_font(size)
		pgImage = font.render(text, True, _COLORS_TO_COMPONENTS.get(color, color))
		width, height = pgImage.get_size()
		imgRes = ImageResources.ImageResource(width, height, False)
		imgRes.image = pgImage
		texture = Graphics2D.GraphicsTexture(imgRes)
		_text[key] = texture
	return texture