class Level:
	
	def __init__(self, name):
		self.name = name
		self.initialize()
		self.sprite_z_sorter = lambda x,y:x.z < y.z
	
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
						referenceStack.append(None)
						tileStack.append(None)
					else:
						t = tilestore.get_tile(cell)
						z = 0
						while z < t.height:
							referenceStack.append(len(tileStack))
							z += 1
						
						tileStack.append(t)
				
			
			i += 1
		self.grid = grid
		self.cellLookup = references
	
	def get_platform_below(self, col, row, z, blocking_only):
	
		# TODO: interlace the block list here
		# so that blocks get included in the collision
		# results
		
		# Alternatively, pushed blocks can be part of the 
		# primary model and will be updated when they move
		# around.
		refStack = self.cellLookup[col][row]
		tileStack = self.grid[col][row]
		i = min(len(refStack) - 1, z // 8)
		
		while i >= 0:
			t = refStack[i]
			if t == None:
				pass
			else:
				tile = self.grid[col][row][t]
				if not blocking_only or tile.blocking:
					return ((i + 1) * 8, tile)
			i -= 1
	
	def render(self, screen, xOffset, yOffset, sprites, render_counter):
		width = self.width
		height = self.height
		sprite_lookup = {}
		for sprite in sprites:
			x = int(sprite.x // 16)
			y = int(sprite.y // 16)
			key = str(x) + '_' + str(y)
			list = sprite_lookup.get(key)
			if list == None:
				list = []
				sprite_lookup[key] = list
			list.append(sprite)
		#print sprite_lookup
		empty_list = []
		
		i = 0
		while i < width + height:
			col = i
			row = 0
			
			while row < height and col >= 0:
				if col < width:
					sprite_list = sprite_lookup.get(str(col) + '_' + str(row))
					
					self.render_tile_stack(screen, col, row, xOffset, yOffset, render_counter, sprite_list)
				row += 1
				col -= 1
			i += 1
	
	def render_sprite(self, screen, sprite, xOffset, yOffset, render_counter):
		platform = sprite.standingon
		img = sprite.get_image(render_counter)
		if platform != None and platform.stairs:
			left = platform.topography[3] * platform.height * 8.0
			right = platform.topography[1] * platform.height * 8.0
			p = sprite.x % 16 + 0.0
			ap = 16.0 - p
			dy = int((left * ap + p * right) / 16.0)
			yOffset -= dy
		coords = sprite.pixel_position(xOffset, yOffset, img)
		screen.blit(img, coords)
	
	def render_tile_stack(self, screen, col, row, xOffset, yOffset, render_counter, sprites):
		stack = self.grid[col][row]
		cumulative_height = 0
		x = xOffset + col * 16 - row * 16 - 16
		y = yOffset + col * 8 + row * 8
		for tile in stack:
			if sprites != None:
				new_sprites = []
				for sprite in sprites:
					if sprite.z < cumulative_height:
						self.render_sprite(screen, sprite, xOffset, yOffset, render_counter)
					else:
						new_sprites.append(sprite)
				sprites = new_sprites
			if tile == None:
				cumulative_height += 8
			else:
				tile.render(screen, x, y - cumulative_height, render_counter)
				cumulative_height += tile.height * 8
		if sprites != None and len(sprites) > 0:
			sprites = safe_sorted(sprites, self.sprite_z_sorter)
			for sprite in sprites:
				self.render_sprite(screen, sprite, xOffset, yOffset, render_counter)
				