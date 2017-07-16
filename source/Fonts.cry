
_COLORS_TO_COMPONENTS = {
	'red': (255, 0, 0),
	'white': (255, 255, 255),
	'black': (0, 0, 0),
}

_defaultFont = None
_text = {}
def get_text(text, size, color):
	key = str(size) + "," + str(color) + "|" + text
	texture = _text.get(key)
	if texture == None:
		size = size * 2 / 3 + 1
		color = _COLORS_TO_COMPONENTS.get(color, color)
		font = _defaultFont if _defaultFont != None else get_default_font()
		fontRenderer = font.getRenderer(size, color[0], color[1], color[2])
		texture = fontRenderer.render(text)
		_text[key] = texture
	return texture

def get_default_font():
	global _defaultFont
	if _defaultFont == None:
		_defaultFont = Graphics2DText.FontResource.fromSystem('Arial')
	return _defaultFont
