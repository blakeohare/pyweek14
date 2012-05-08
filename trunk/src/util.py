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

def max(a, b):
	if a < b:
		return b
	return a
	
def min(a, b):
	if a < b:
		return a
	return b

_range_4 = [0, 1, 2, 3]
_range_2 = [0, 1]
def safe_range(x):
	global _range_4, _range_2
	if x < 10:
		if x == 4:
			return _range_4
		if x == 2:
			return _range_2
	
	output = [0] * x
	i = 1
	while i < x:
		output[i] = i
		i += 1
	return output

def safe_sorted(list, compare):
	if len(list) <= 1:
		return list
	if len(list) == 2:
		if compare(list[0], list[1]):
			return list
		else:
			return list[::-1]
	pivot = list[len(list) // 2]
	left = []
	right = []
	for item in list:
		if compare(item, pivot):
			left.append(item)
		else:
			right.append(item)
	
	left = safe_sorted(left, compare)
	right = safe_sorted(right, compare)
	return left + right

_assertions_break = True
def assertion(message):
	global _assertions_break
	print(message)
	if _assertions_break:
		destroy = 1 / 0

def copy_array(target, source):
	while len(target) > len(source):
		target.pop()
	while len(target) < len(source):
		target.append(None)
	
	i = 0
	while i < len(source):
		target[i] = source[i]
		i += 1
def debug_dict(dictionary):
	return '\n'.join(safe_map(lambda k:str(k) + ": " + str(dictionary[k]), dictionary.keys()))

def debug_list(list):
	return '\n'.join(safe_map(str, list))