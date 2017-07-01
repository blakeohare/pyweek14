_image_library = {}
_imageSheet = None

def get_image(path):
	image = _image_library.get(path)
	if image == None:
		imageRes = _imageSheet.getImage(canonicalize_path('images/' + path))
		image = Graphics2D.GraphicsTexture.load(imageRes)
		_image_library[path] = image
	return image
