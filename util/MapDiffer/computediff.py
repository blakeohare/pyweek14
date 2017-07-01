import os


def trim(string):
	while len(string) > 0 and string[0] in ' \r\n\t':
		string = string[1:]
	while len(string) > 0 and string[-1] in ' \r\n\t':
		string = string[:-1]
	return string

python3 = 5 / 2 == 2.5

get_input = input if python3 else raw_input

print("Map without the action:")
mapA = get_input()
print("Map with the action:")
mapB = get_input()
print("Name of action (No colons, tabs, spaces or | character):")
action_name = get_input()

def can_path(path):
	path = '../../' + path
	path = path.replace('/', os.sep).replace('\\', os.sep)
	return path

def read_file(path):
	path = can_path(path)
	c = open(path, 'rt')
	t = c.read()
	c.close()
	return t

def generate_tile_store():
	files = os.listdir(can_path('data/tile_manifests'))
	tiles = {}
	for file in files:
		if '.svn' in file: continue
		lines = Resources.readText('data/tile_manifests/' + file).split('\n')
		for line in lines:
			parts = line.split('\t')
			if len(parts) > 3:
				id = parts[0]
				height = int(parts[2])
				tiles[id] = height
	tiles['0'] = 1
	return tiles

tile_store = generate_tile_store()	

def get_tile_height(id):
	global tile_store
	
	output = tile_store.get(id)
	return output

def read_map_file(name):
	t = Resources.readText('data/levels/' + name + '.txt')
	
	lines = t.split('\n')
	values = {}
	
	for line in lines:
		parts = trim(line).split(':')
		if len(parts) >= 2 and len(parts[0]) > 0 and parts[0][0] == '#':
			key = parts[0][1:]
			value = ':'.join(parts[1:])
			values[key] = trim(value)
	
	tiles = values.get('tiles', None)
	
	
	
	width = int(values['width'])
	height = int(values['height'])
	
	cells = tiles.split(',')
	output = []
	for cell in cells:
		x = []
		output.append(x)
		if len(cell) > 0:
			tiles = cell.split('|')
			for tile in tiles:
				t_height = get_tile_height(tile)
				x.append(tile)
				while t_height > 1:
					x.append('0')
					t_height -= 1
	return (width, output, values)

tilesA = read_map_file(mapA)
tilesB = read_map_file(mapB)

def compute_diff(a, b):
	width = a[0]
	a = a[1]
	b = b[1]
	i = 0
	pchanges = []
	nchanges = []
	while i < len(a):
		col = i % width
		row = i // width
		pchanges = pchanges + compute_stack_diff(col, row, a[i][:], b[i][:])
		nchanges = nchanges + compute_stack_diff(col, row, b[i][:], a[i][:])
		i += 1
	
	return (pchanges, nchanges)

def compute_stack_diff(col, row, a, b):
	
	while len(a) < len(b):
		a.append('0')
	while len(b) < len(a):
		b.append('0')
	
	for q in (a, b):
		if len(q) == 0: q.append('0')
		
		for i in range(get_tile_height(q[-1]) - 1):
			q.append('0')
	
		
	
	changes = []
	
	i = 0
	while i < len(a):
		if a[i] != b[i]:
			changes.append((col, row, i, b[i]))
			a_height = get_tile_height(b[i])
			b_height = get_tile_height(b[i])
			for j in range(b_height):
				b[i + j] = '0'
			for j in range(a_height):
				a[i + j] = '0'
			b[i] = a[i]
		i += 1
	return changes


pdiff,ndiff = compute_diff(tilesA, tilesB)

def make_diff_value(diff):
	output = []
	for d in diff:
		output.append(str(d[0]) + '^' + str(d[1]) + '^' + str(d[2]) + '^' + d[3])
	return '%'.join(output)

values = tilesA[2]
values['action|positive|' + action_name] = make_diff_value(pdiff)
values['action|negative|' + action_name] = make_diff_value(ndiff)

output = []
for key in values.keys():
	value = values[key]
	line = '#' + key + ':' + value
	output.append(line)

output = '\r\n'.join(output)

c = open(can_path('data/levels/' + mapA + '.txt'), 'wt')
c.write(output)
c.close()

print("Done!")