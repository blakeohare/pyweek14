class Level:
	
	def __init__(self, name):
		self.name = name
		self.initialize()
	
	def initialize(self):
		lines = read_file('data/levels/' + self.name + '.txt').split('\n')
		values = {}
		for line in lines:
			line = trim(line)
			if len(line) > 0 and line[0] == '#':
				parts = line.split(':')
				if len(parts) > 1:
					key = parts[0][1:]
					value = ':'.join(parts[1:])
					values[key] = value
		self.values = values
		
		self.width = int(self.values['width'])
		self.height = int(self.values['height'])
		self.initialize_tiles(self.values['tiles'].split(','))
	
	def initialize_tiles(self, tiles):
		width = self.width
		height = self.height
		grid = make_grid(self.width, self.height, None)
		references = make_grid(self.width, self.height, None)
		
		tilestore = get_tile_store()
		i = 0
		for tile in tiles:
			x = i % width
			y = i // width
			tileStack = []
			referenceStack = []
			grid[x][y] = tileStack
			references[x][y] = referenceStack
			cells = tile.split('|')
			
			if len(cells) == 1 and len(cells[0]) == 0:
				pass
			else:
				for cell in cells:
					
					if cell == '0':
						referenceStack.append(len(tileStack))
						tileStack.append(None)
					else:
						t = tilestore.get_tile(cell)
						z = 0
						while z < t.height:
							referenceStack.append(len(tileStack) - 1)
							z += 1
						
						tileStack.append(t)
				
			
			i += 1
		self.grid = grid
		self.cellLookup = references
	
	def render(self, screen, xOffset, yOffset, render_counter):
		
		i = 0
		width = self.width
		height = self.height
		while i < width + height:
			col = i
			row = 0
			while row < height and col >= 0:
				if col < width:
					self.render_tile_stack(screen, col, row, xOffset, yOffset, render_counter)
				row += 1
				col -= 1
			i += 1
	
	def render_tile_stack(self, screen, col, row, xOffset, yOffset, render_counter):
		stack = self.grid[col][row]
		cumulative_height = 0
		x = xOffset + col * 16 - row * 16
		y = yOffset + col * 8 + row * 8
		for tile in stack:
			if tile == None:
				cumulative_height += 8
			else:
				tile.render(screen, x, y - cumulative_height, render_counter)
				cumulative_height += tile.height * 8
		