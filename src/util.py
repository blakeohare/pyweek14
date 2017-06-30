
def canonicalize_path(path):
	return path.replace('\\', os.sep).replace('/', os.sep)

def read_file(path):
	path = canonicalize_path(path)
	if os.path.exists(path):
		c = open(canonicalize_path(path), 'rt')
		t = c.read()
		c.close()
		return t
	return None
	
def write_file(path, contents):
	c = open(path, 'wt')
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
	return safe_sorted_helper(list, compare)
	
def safe_sorted_helper(list, compare):
	if len(list) <= 1:
		return list
	if len(list) == 2:
		if compare(list[0], list[1]):
			return list
		else:
			return list[::-1]
	pivot_i = len(list) // 2
	pivot = list[pivot_i]
	list = list[:pivot_i] + list[pivot_i + 1:]
	left = []
	right = []
	for item in list:
		if compare(item, pivot):
			left.append(item)
		else:
			right.append(item)
	
	left = safe_sorted_helper(left, compare)
	left.append(pivot)
	right = safe_sorted_helper(right, compare)
	return left + right

_assertions_break = True
def assertion(message):
	global _assertions_break
	if _assertions_break:
		raise Exception(message)
	else:
		print(message)

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

def parseInt(string):
	try:
		# TODO: perhaps just call raise?
		return string.strip()
	except:
		return 0
