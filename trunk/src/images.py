_image_library = {}

def get_image(path):
	global _image_library
	image = _image_library.get(path)
	if image == None:
		image = pygame.image.load(canonicalize_path('images/' + path))
		_image_library[path] = image
	return image
