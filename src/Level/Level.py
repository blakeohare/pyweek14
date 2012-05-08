class Level:
	
	def __init__(self, name):
		self.name = name
		self.initialize()
		self.sprite_z_sorter = lambda x,y:x.z < y.z
		self.push_counter = -1
		self.max_push_counter = 25
		self.push_target = None
		self.newsprites = []
		
	
	def get_new_sprites(self):
		output = self.newsprites
		self.newsprites = []
		return output
	
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
	
	# there are no blockages. It's already been verified by the time this function
	# has been called.
	def push_block(self, start_col, start_row, end_col, end_row, layer):
		play_sound('blockpush.wav')
		self.push_counter = -1
		self.push_target = None
		
		block = self.modify_block(start_col, start_row, layer, None)
		self.modify_block(end_col, end_row, layer, block)
		
		target_lookup = self.cellLookup[end_col][end_row]
		stack = self.grid[end_col][end_row]
		below_layer = layer - 1
		should_spritify = False
		if below_layer < len(target_lookup):
			standingon = target_lookup[below_layer]
			if standingon == None:
				should_spritify = True
			else:
				standingon = stack[standingon]
				if not standingon.blocking:
					should_spritify = True
		else:
			should_spritify = True
		
		if should_spritify:
			self.modify_block(end_col, end_row, layer, None)
			self.newsprites.append(Sprite(end_col * 16 + 8, end_row * 16 + 8, layer * 8, 'block|' + block.id))
		
	
	def modify_block(self, col, row, layer, type):
		output = None
		z = 0
		stack = self.grid[col][row]
		newstack = []
		layer_bottom = layer
		layer_top = layer
		if type != None:
			layer_top += type.height - 1
		
		for item in stack:
			if item == None:
				newstack.append(None)
				z += 1
			else:
				
				if z >= layer_bottom and z <= layer_top:
					if z == layer_bottom:
						output = item
					newstack += [None] * item.height
				else:
					newstack.append(item)
				z += item.height
		while z <= layer_top:
			newstack.append(None)
			z += 1
		# at this point newstack has all None's where the modification will go
		
		i = 0
		z = 0
		while i < len(newstack):
			item = newstack[i]
			if z == layer_bottom:
				newstack[i] = type
				for q in range(layer_top - layer_bottom):
					newstack.pop(i + 1)
				break
			if item == None:
				z += 1
			else:
				z += item.height
			i += 1
		
		copy_array(stack, newstack)
		
		self.canonicalize_stack(col, row)
		return output
	
	def canonicalize_stack(self, col, row):
		stack = self.grid[col][row]
		lookup = []
		i = 0
		for item in stack:
			if item == None:
				lookup.append(None)
			else:
				lookup += [i] * item.height
			i += 1
		copy_array(self.cellLookup[col][row], lookup)
		