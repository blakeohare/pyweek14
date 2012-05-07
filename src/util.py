def trim(string):
	while len(string) > 0 and string[0] in ' \n\r\t':
		string = string[1:]
	while len(string) > 0 and string[-1] in ' \r\n\t':
		string = string[:-1]
	return string

def canonicalize_path(path):
	return path.replace('\\', os.sep).replace('/', os.sep)

def read_file(path):

	c = open(canonicalize_path(path), 'rt')
	t = c.read()
	c.close()
	return t
	
def write_file(path, contents):
	c = open(canonicalize_path(path), 'wt')
	c.write(contents)
	c.close()

def make_grid(width, height, defaultValue):
	cols = []
	x = 0
	while x < width:
		col = []
		y = 0
		while y < height:
			col.append(defaultValue)
			y += 1
		cols.append(col)
		x += 1
	return cols

def safe_map(function, list):
	i = 0
	l = len(list)
	output = []
	while i < l:
		output.append(function(list[i]))
		i += 1
	return output
