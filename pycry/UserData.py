import os

# TODO: this all just reads the local current directory

def _getUserDirectory():
	return '.'

def _canonicalizePath(path):
	return os.path.join(_getUserDirectory(), path).replace('/', os.sep).replace('\\', os.sep)
	
def fileReadText(path):
	path = _canonicalizePath(path)
	c = open(path, 'rt')
	text = c.read()
	c.close()
	return text

def fileExists(path):
	path = _canonicalizePath(path)
	return os.path.exists(path) and not os.path.isdir(path)

def fileWriteText(path, text):
	path = _canonicalizePath(path)
	c = open(path, 'wt')
	c.write(text)
	c.close()
