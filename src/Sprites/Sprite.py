class Sprite:
	# sprite coordinates are assuming the grid is 16x16 tiles
	# these get transposed into pixel coordinates and
	# are converted into tile coords by simply dividing by 16
	def __init__(self, x, y, z, type):
		self.x = x + 0.0
		self.y = y + 0.0
		self.z = z
		self.dx = 0
		self.dy = 0
		self.dz = 0
		self.standingon = None
		self.ismain = type == 'main'
		self.height = 4
	
	def get_image(self, render_counter):
		img = get_image('temp_sprite.png')
		return img
	
	def pixel_position(self, xOffset, yOffset, img):
		x = self.x - self.y
		y = (self.x + self.y) / 2
		x = x - img.get_width() / 2
		y = y - self.z - img.get_height() + 8
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
			self.dz = -3

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
				pass # if we were cool with it before, we're cool with it now
			elif starting_col != ending_col and starting_row != ending_row:
				# player moved diagonally to another tile and skipped over intermediate tiles
				# check one of the tiles between to make sure there's a path.
				check_these.append((ending_col, starting_row))
				check_these.append((ending_col, ending_row))
			else:
				# player moved to a tile cardinally next to it
				check_these.append((ending_col, ending_row))
			
			blocked = False
			clearance = safe_range(self.height)
			cellLookup = level.cellLookup
			tilestack = level.grid
			new_platform = self.standingon
			for check in check_these:
				col = check[0]
				row = check[1]
				lookup = cellLookup[col][row]
				tiles = tilestack[col][row]
				for c in clearance:
					if len(lookup) > c + layer and lookup[c + layer] != None:
						if tiles[lookup[c + layer]].blocking:
							#TODO: add a shove counter if it's pushable
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
				tile = level.grid[col][row][lookup[layer]]
				if tile.blocking:
					self.standingon = tile
				else:
					self.standingon = None
			else:
				self.standingon = None
		
		self.dx = 0
		self.dy = 0
		self.dz = 0
		