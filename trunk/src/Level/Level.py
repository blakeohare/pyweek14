class Level:
	
	def __init__(self, name):
		self.name = name
		self.initialize()
		self.sprite_z_sorter = lambda x,y:x.z < y.z
		self.push_counter = -1
		self.max_push_counter = 25
		self.push_target = None
		self.newsprites = []
		self.circuitry = Circuits(self)
		self.render_exceptions = []
		self.moving_platforms = MovingPlatformManager(self)
		self.teleporters = TeleporterManager(self)
	
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
		moving_platforms = []
		self.teleporter_tiles = []
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
						if t.id == '16': # moving platform
							moving_platforms.append((x, y, len(referenceStack)))
						if t.id in ('t1', 't2', 't3'):
							self.teleporter_tiles.append((x, y, len(referenceStack), t.id))
						z = 0
						while z < t.height:
							referenceStack.append(len(tileStack))
							z += 1
						
						tileStack.append(t)
				
			
			i += 1
		self.grid = grid
		self.cellLookup = references
		self.moving_platforms = moving_platforms
		
	def get_tile_at(self, x, y=None, z=None):
		if y == None:
			y = x[1]
			z = x[2]
			x = x[0]
		lookup = self.cellLookup[x][y]
		if len(lookup) <= z:
			return None
		index = lookup[z]
		if index == None:
			return None
		return self.grid[x][y][index]
	
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
	
	def render(self, screen, xOffset, yOffset, sprites, render_counter, sprites_to_add, sprites_to_delete):
		self.allsprites = sprites
		
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
		empty_list = []
		
		re_on_keys = {}
		re_off_keys = {}
		for re in self.render_exceptions:
			re_on_keys[re.on_key] = re_on_keys.get(re.on_key, [])
			re_on_keys[re.on_key].append(re)
			re_off_keys[re.off_key] = re_off_keys.get(re.off_key, [])
			re_off_keys[re.off_key].append(re)
		
		z_sorter = lambda a,b: a.z < b.z
		for k in re_on_keys.keys():
			re_on_keys[k] = safe_sorted(re_on_keys[k], z_sorter)
		for k in re_off_keys.keys():
			re_off_keys[k] = safe_sorted(re_off_keys[k], z_sorter)
		
		i = 0
		while i < width + height:
			col = i
			row = 0
			
			while row < height and col >= 0:
				if col < width:
					sprite_list = sprite_lookup.get(str(col) + '_' + str(row))
					k = str(col) + '|' + str(row)
					re_on = re_on_keys.get(k)
					re_off = re_off_keys.get(k)
					
					if re_on != None:
						re_on = re_on[:]
					if re_off != None:
						re_off = re_off[:]
					
					self.render_tile_stack(screen, col, row, xOffset, yOffset, render_counter, sprite_list, re_on, re_off)
				row += 1
				col -= 1
			i += 1
		
		self.update(sprites, sprites_to_add, sprites_to_delete)
	
	def render_sprite(self, screen, sprite, xOffset, yOffset, render_counter):
		sprite.render_me(screen, xOffset, yOffset, render_counter)
	
	def render_tile_stack(self, screen, col, row, xOffset, yOffset, render_counter, sprites, re_on, re_off):
		re_sprite_on = None
		re_sprite_off = None
		re_block_on = None
		re_block_off = None
		
		if re_on != None:
			re_block_on = []
			re_sprite_on = []
			for re in re_on:
				if re.is_block:
					re_block_on.append(re)
				else:
					re_sprite_on.append(re)
			
		if re_off != None:
			re_block_off = []
			re_sprite_off = []
			for re in re_off:
				if re.is_block:
					re_block_off.append(re)
				else:
					re_sprite_off.append(re)				
		
		prefix = str(col) + '|' + str(row) + '|'
		
		stack = self.grid[col][row]
			
		z = 0
		x = xOffset + col * 16 - row * 16 - 16
		y = yOffset + col * 8 + row * 8
		i = 0
		while i < len(stack):
			tile = stack[i]
			if sprites != None:
				new_sprites = []
				for sprite in sprites:
					if sprite.z <= z * 8:
						if re_sprite_off != None and len(re_sprite_off) > 0 and re_sprite_off[0].z == z and re_sprite_off[0].tile == sprite:
							re = re_sprite_off.pop(0)
						else:
							re_offset = (0, 0)
							if re_sprite_on != None:
								rei = 0
								while rei < len(re_sprite_on):
									re = re_sprite_on[rei]
									if re.tile == sprite:
										re_sprite_on.pop(rei)
										re_offset = re.get_offset()
									else:
										rei += 1
							self.render_sprite(screen, sprite, xOffset + re_offset[0], yOffset + re_offset[1], render_counter)
					else:
						new_sprites.append(sprite)
				sprites = new_sprites
			
			while re_sprite_on != None and len(re_sprite_on) > 0 and re_sprite_on[0].z < z:
				re = re_sprite_on.pop(0)
				offset = re.get_offset()
				_x = xOffset + offset[0]
				_y = yOffset + offset[1]
				xdiff = re.do_show[0] - re.dont_show[0]
				ydiff = re.do_show[1] - re.dont_show[1]
				xdiff_pixel = xdiff * 16 - ydiff * 16
				ydiff_pixel = xdiff * 8 + ydiff * 8
				self.render_sprite(screen, re.tile, _x + xdiff_pixel, _y + ydiff_pixel, render_counter)
			
			if tile == None:
				if re_block_on != None and len(re_block_on) > 0 and re_block_on[0].z == z:
					re = re_block_on.pop(0)
					offset = re.get_offset()
					re.tile.render(screen, x + offset[0], y - z * 8 + offset[1], render_counter)
					#z += re.tile.height - 1
				z += 1
			else:
				if re_block_off != None and len(re_block_off) > 0 and re_block_off[0].z == z:
					re = re_block_off.pop(0)
				elif re_block_on != None and len(re_block_on) > 0 and re_block_on[0].z == z:
					re = re_block_on.pop(0)
					offset = re.get_offset()
					tile.render(screen, x + offset[0], y - z * 8 + offset[1], render_counter)
				else:
					tile.render(screen, x, y - z * 8, render_counter)
				z += tile.height
			i += 1
		if (sprites != None and len(sprites) > 0) or (re_sprite_on != None and len(re_sprite_on) > 0):
			sprites = [] if sprites == None else safe_sorted(sprites, self.sprite_z_sorter)
			sprite_i = 0
			re_i = 0
			if re_sprite_on == None:
				re_sprite_on = []
			
			rendered_sprites = []
			for re in re_sprite_on:
				for sprite in sprites:
					if re.tile == sprite:
						rendered_sprites.append(sprite)
			if len(rendered_sprites) > 0:
				new_sprites = []
				for sprite in rendered_sprites:
					if sprite in rendered_sprites:
						pass
					else:
						new_sprites.append(sprite)
				sprites = new_sprites
			
			while sprite_i < len(sprites) or re_i < len(re_sprite_on):
				sprite = None
				re = None
				if sprite_i == len(sprites):
					re = re_sprite_on[re_i]
					re_i += 1
				elif re_i == len(re_sprite_on):
					sprite = sprites[sprite_i]
					sprite_i += 1
				else:
					re = re_sprite_on[re_i]
					sprite = sprites[sprite_i]
					if re.z < int(sprite.z // 8):
						sprite = None
						re_i += 1
					else:
						re = None
						sprite_i += 1
				
				if re != None:
					offset = re.get_offset()
					_x = xOffset + offset[0]
					_y = yOffset + offset[1]
					if re.direction == 'NE' or re.direction == 'NW':
						xdiff = re.do_show[0] - re.dont_show[0]
						ydiff = re.do_show[1] - re.dont_show[1]
						xdiff_pixel = xdiff * 16 - ydiff * 16
						ydiff_pixel = xdiff * 8 + ydiff * 8
						_x += xdiff_pixel
						_y += ydiff_pixel
					
					self.render_sprite(screen, re.tile, _x, _y, render_counter)

				else:
					suppress = False
					if re_sprite_off != None:
						rei = 0
						while rei < len(re_sprite_off):
							re = re_sprite_off[rei]
							if sprite == re.tile:
								re_sprite_off.pop(rei)
								suppress = True
							else:
								rei += 1
					if not suppress:
						self.render_sprite(screen, sprite, xOffset, yOffset, render_counter)
	
	# there are no blockages. It's already been verified by the time this function
	# has been called.
	def push_block(self, start_col, start_row, end_col, end_row, layer):
		play_sound('blockpush.wav')
		self.push_counter = -1
		self.push_target = None
		
		block = self.modify_block(start_col, start_row, layer, None)
		self.modify_block(end_col, end_row, layer, block)
		
		if start_row == end_row:
			if start_col < end_col:
				dir = 'SE'
			else:
				dir = 'NW'
		elif start_row < end_row:
			dir = 'SW'
		else:
			dir = 'NE'
			
		self.render_exceptions.append(RenderException((start_col, start_row, layer), dir, block, True))
		
		below_layer = layer - 1
		
		was_standing_on = self.get_tile_at(start_col, start_row, below_layer)
		
		target_lookup = self.cellLookup[end_col][end_row]
		stack = self.grid[end_col][end_row]
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
					if standingon.id == 'po' and block.id == '46' and self.circuitry.is_charged(end_col, end_row, below_layer):
						play_sound('battery_charge.wav')
						self.modify_block(end_col, end_row, layer, get_tile_store().get_tile('45'))
					if standingon.id == 'pi':
						if block.id == '45':
							#play_sound('electricity_flows.wav')
							self.circuitry.refresh_charges()
					if was_standing_on != None and was_standing_on.id == 'pi' and block.id == '45':
						play_sound('battery_deplete.wav')
						self.modify_block(end_col, end_row, layer, get_tile_store().get_tile('46'))
						self.circuitry.refresh_charges()
						
		else:
			should_spritify = True
		
		if should_spritify:
			self.spritify_block(end_col, end_row, layer)
	
	def spritify_block(self, col, row, layer):
		block = self.modify_block(col, row, layer, None)
		self.newsprites.append(Sprite(col * 16 + 8, row * 16 + 8, layer * 8, 'block|' + block.id))
		
	
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
		
		teleported = False
		if type != None and type.pushable:
			# check to see if we just placed a pushable block onto a teleporter platform
			t = self.get_tile_at(col, row, layer - 1)
			if t != None and t.teleporter:
				d = self.teleporters.get_destination(col, row, layer - 1)
				if d == 'blocked':
					self.announce_teleporter_blocked()
				elif d == None:
					pass
				else:
					teleported = True
					source = (col, row, layer)
					self.teleporters.teleport_block(type, source, d)
		
		if not teleported:
			copy_array(stack, newstack)
			self.canonicalize_stack(col, row)
		
		return output
	
	def announce_teleporter_blocked(self):
		pass
		# TODO: play sound
	
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
	
	def update(self, sprites, sprite_additions, sprite_removals):
		new_re = []
		self.moving_platforms.update(sprites, new_re)
		self.teleporters.update()
		
		for sprite in self.teleporters.get_new_sprites():
			sprite_additions.append(sprite)
		for sprite in self.teleporters.get_removed_sprites():
			sprite_removals.append(sprite)
		
		
		for re in self.render_exceptions:
			re.update()
			if not re.expired:
				new_re.append(re)
		self.render_exceptions = new_re
		
	
	def get_moving_platforms(self):
		return self.moving_platforms
	
	def get_teleporters(self):
		return self.teleporter_tiles
	