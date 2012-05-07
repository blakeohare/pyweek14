_block_images_for_sprites = None

class Sprite:
	# sprite coordinates are assuming the grid is 16x16 tiles
	# these get transposed into pixel coordinates and
	# are converted into tile coords by simply dividing by 16
	def __init__(self, x, y, z, type):
		global _block_images_for_sprites
		self.garbage_collect = False
		self.x = x + 0.0
		self.y = y + 0.0
		self.z = z
		self.dx = 0
		self.dy = 0
		self.dz = 0
		self.standingon = None
		self.ismain = type == 'main'
		self.height = 4
		self.isblock = type.startswith('block|')
		
		if _block_images_for_sprites == None:
			tile_store = get_tile_store()
			ids = tile_store.get_all_block_tiles()
			_block_images_for_sprites = {}
			for id in ids:
				_block_images_for_sprites[id] = tile_store.get_tile(id)
		
		if self.isblock:
			self.block_id = type.split('|')[-1] # should be the tile ID
			self.block_tile = get_tile_store().get_tile(self.block_id)
		
	
	def get_image(self, render_counter):
		img = None
		if self.ismain:
			img = get_image('temp_sprite.png')
		elif self.isblock:
			img = self.block_tile.get_image(render_counter)
		return img
	
	def pixel_position(self, xOffset, yOffset, img):
		x = self.x - self.y
		y = (self.x + self.y) / 2
		x = x - img.get_width() / 2
		y = y - self.z - img.get_height() + 8
		if self.isblock:
			y += 8
		output = (int(x + xOffset), int(y + yOffset))
		
		return output
	
	def debug_stats(self):
		return ' '.join(safe_map(str, [
			'x:', self.x,
			'y:', self.y,
			'z:', self.z,
			'dx:', self.dx,
			'dy:', self.dy,
			'dz:', self.dz]))
		
	
	def update(self, level):
		if self.standingon == None:
			self.dz = -1

		if self.dz != 0:
			platform_data = level.get_platform_below(int(self.x) // 16, int(self.y) // 16, self.z, True)
			if platform_data != None:
				z = platform_data[0]
				platform = platform_data[1]
				if z < self.dz + self.z:
					self.z += self.dz
				else:
					self.z = z
					self.standingon = platform
			else:
				self.standingon = None
				self.z += self.dz
		layer = self.z // 8
		
		if self.dz == 0:
			starting_col = int(self.x) // 16
			starting_row = int(self.y) // 16
			
			ending_col = int(self.x + self.dx) // 16
			ending_row = int(self.y + self.dy) // 16
			
			check_these = []
			if starting_col == ending_col and starting_row == ending_row:
				# if we were cool with it before, we're cool with it now
				direction = None
				opposite = None
			elif starting_col != ending_col and starting_row != ending_row:
				# player moved diagonally to another tile and skipped over intermediate tiles
				# check one of the tiles between to make sure there's a path.
				check_these.append((ending_col, starting_row))
				check_these.append((ending_col, ending_row))
				if starting_col < ending_col:
					if starting_row < ending_row:
						direction = 'S'
						opposite = 'N'
					else:
						direction = 'E'
						opposite = 'W'
				else:
					if starting_row < ending_row:
						direction = 'W'
						opposite = 'E'
					else:
						direction = 'N'
						opposite = 'S'
			else:
				# player moved to a tile cardinally next to it
				check_these.append((ending_col, ending_row))
				if starting_col == ending_col:
					if starting_row < ending_row:
						direction = 'SW'
						opposite = 'NE'
					else:
						direction = 'NE'
						opposite = 'SW'
				else:
					if starting_col < ending_col:
						direction = 'SE'
						opposite = 'NW'
					else:
						direction = 'NW'
						opposite = 'SE'
			
			blocked = False
			topToBottom = True
			clearance = safe_range(self.height)[:]
			if topToBottom:
				clearance = clearance[::-1]
			cellLookup = level.cellLookup
			tilestack = level.grid
			new_platform = self.standingon
			for check in check_these:
				col = check[0]
				row = check[1]
				if col < 0 or col >= level.width or row < 0 or row >= level.height:
					blocked = True
					break
				lookup = cellLookup[col][row]
				tiles = tilestack[col][row]
				for c in clearance:
					if len(lookup) > c + layer and lookup[c + layer] != None:
						tz = lookup[c + layer]
						t = tiles[tz]
						
						if t.blocking:
							if self.ismain:
								prev_push_target = level.push_target
								level.push_target = None
								if t.pushable and direction != None and len(direction) == 2:
									blocked = True
									push_key = str(col) + '^' + str(row) + '^' + str(tz)
									level.push_target = push_key
									if push_key == prev_push_target:
										level.push_counter -= 1
									else:
										level.push_counter = level.max_push_counter
									if level.push_counter == 0:
										# Try to do the push
										if direction == 'NW':
											tcol = col - 1
											trow = row
										elif direction == 'NE':
											tcol = col
											trow = row - 1
										elif direction == 'SW':
											tcol = col
											trow = row + 1
										elif direction == 'SE':
											tcol = col + 1
											trow = row
										else:
											assertion("ERROR: bad direction while pushing block.")
										
										if tcol >= 0 and tcol < level.width and trow >= 0 and trow < level.height:
											tlookup = level.cellLookup[tcol][trow]
											tstack = level.grid[tcol][trow]
											bottom_free = True
											top_free = True
											bottom_index = c + layer - 1
											top_index = c + layer
											
											if len(tlookup) > bottom_index:
												bottom_index = tlookup[bottom_index]
												if bottom_index != None and tstack[bottom_index].blocking:
													bottom_free = False
											
											if len(tlookup) > top_index:
												top_index = tlookup[top_index]
												if top_index != None and tstack[top_index].blocking:
													top_free = False
											
											if bottom_free and top_free:
												level.push_block(col, row, tcol, trow, c + layer - 1)
											else:
												level.push_counter = -1
												level.push_target = None
											break
										else:
											level.push_counter = -1
											level.push_target = None
									
								
							# The target tile will always be last in check_these
							if blocked == False and t.stairs and t.entrance == opposite and check == check_these[-1]:
								if c == 0:
									# not blocked
									zbefore = self.z
									self.z += t.height * 8
									break
							else:
								blocked = True
								break
				if blocked:
					break
				
			if not blocked:
				self.x += self.dx
				self.y += self.dy
		
		if self.dz == 0:
			col = int(self.x // 16)
			row = int(self.y // 16)
			layer = int(self.z - 1) // 8
			lookup = level.cellLookup[col][row]
			if layer < len(lookup):
				_t = lookup[layer]
				if _t == None:
					self.standingon = None
				else:
					tile = level.grid[col][row][_t]
					if tile.blocking:
						self.standingon = tile
					else:
						self.standingon = None
			else:
				self.standingon = None
		
		if self.isblock and self.standingon != None:
			# turn me back into a real block
			self.garbage_collect = True
			level.modify_block(int(self.x // 16), int(self.y // 16), int(self.z // 8), self.block_tile)
		
		self.dx = 0
		self.dy = 0
		self.dz = 0
		