import os

def _canonicalizePath(dir):
	return dir.replace('\\', os.sep).replace('/', os.sep)

def directoryExists(dir):
	dir = _canonicalizePath(dir)
	return os.path.exists(dir) and os.path.isdir(dir)

def directoryList(dir, includeFullPath = False):
	dir = _canonicalizePath(dir)
	if dir[-1:] == os.sep:
		dir = dir[:-1]
	if dir[:1] == os.sep:
		dir = dir[1:]
	files = os.listdir(dir)
	if includeFullPath:
		slashDir = dir.replace(os.sep, '/')
		for i in range(len(files)):
			files[i] = slashDir + '/' + files[i]
	return files

def fileExists(path):
	path = _canonicalizePath(path)
	return os.path.exists(path) and not os.path.isdir(path)

def readText(path):
	path = _canonicalizePath(path)
	c = open(path, 'rt')
	text = c.read()
	c.close()
	return text
