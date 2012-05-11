_block_images_for_sprites = None
_surface_cache = {}

def get_surface(width, height):
	global _surface_cache
	k = str(width) + '|' + str(height)
	surface = _surface_cache.get(k, None)
	if surface == None:
		surface = pygame.Surface((width, height)).convert()
		_surface_cache[k] = surface
	return surface
	
def get_teleporter_image(going_out, counter, type):
	counter = min(60, max(0, counter))
	if going_out:
		counter = 60 - counter
	
	if counter < 30:
		ao = 255 - counter * 255 / 30
		bo = 255
	else:
		ao = 0
		bo = (60 - counter) * 255 / 30
	if type == 'main':
		imgs = (
			get_image('protagonist/s.png'),
			get_image('static/character' + str((int(counter // 2) % 4) + 1) + '.png'))
	else:
		block_id = type[len('block|'):]
		if going_out and counter < 6:
			return None
		ts = get_tile_store()
		imgs = (
			ts.get_tile(block_id).get_image(counter),
			get_image('static/block' + str((int(counter // 2) % 4) + 1) + '.png'))

	return (ao, bo, imgs[0], imgs[1])
	

def copy_surface(surface):
	return pygame.Surface(surface)

def blit_at_opacity(target, source, x, y, opacity):
	t = get_surface(source.get_width(), source.get_height())
	t.blit(screen, (-x, -y))
	t.blit(source)
	t.set_alpha(opacity)
	screen.blit(t, (x, y))

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
		self.automation = None
		self.falling = False
		self.standingon = None
		self.type = type
		self.immobilized = False
		self.spray_counter = -1
		self.ismain = type == 'main'
		self.main_or_hologram = self.ismain or type == 'hologram|main'
		self.isjanitor = type == 'janitor'
		self.holding_spray = False
		self.holding_walkie = False
		self.issupervisor = type == 'supervisor'
		self.isblock = type.startswith('block|')
		self.israt = type.startswith('rat')
		self.rat_trot_mode = None
		if self.israt:
			self.type = 'rat'
			
		
		self.death_counter = -1
		self.death_type = None
		self.height = 4
		if self.isblock:
			self.height = 2
		self.tsend = type.startswith('teleport|')
		self.trecv = type.startswith('receiving|')
		self.staticy = self.tsend or self.trecv
		self.ttype = None
		if self.staticy:
			self.ttype = '|'.join(type.split('|')[1:])
		self.ttl = None
		if self.staticy:
			self.ttl = 60
		self.last_direction_of_movement = 's'
		self.direction_queue = ['s']
		self.is_moving = False
		self.pushing = None
		if self.isblock:
			self.height = 2
		
		if _block_images_for_sprites == None:
			tile_store = get_tile_store()
			ids = tile_store.get_all_block_tiles()
			_block_images_for_sprites = {}
			for id in ids:
				_block_images_for_sprites[id] = tile_store.get_tile(id)
		
		if self.isblock:
			self.block_id = type.split('|')[-1] # should be the tile ID
			self.block_tile = get_tile_store().get_tile(self.block_id)
		
	
	def set_automation(self, automation):
		self.automation = automation
		automation.sprite = self
	
	
	def render_me(self, screen, xOffset, yOffset, render_counter):
		img = self.get_image(render_counter)
		coords = self.pixel_position(xOffset, yOffset, img)
		
		if self.staticy:
			things = get_teleporter_image(self.tsend, self.ttl, self.ttype)
			if things == None: return
			ao = things[0]
			bo = things[1]
			ai = things[2]
			bi = things[3]
			
			for x in ((bo, bi), (ao, ai)):
				o = x[0]
				img = x[1]
				
				if o > 0:
					t = get_surface(img.get_width(), img.get_height())
					t.blit(screen, (-coords[0], -coords[1]))
					t.blit(img, (0, 0))
					t.set_alpha(o)
					screen.blit(t, (coords[0], coords[1]))	
		else:
			screen.blit(img, coords)
		
	
	
	def get_image(self, render_counter):
		img = None
		if self.ismain:
			if self.death_counter > 0:
				path = 'protagonist/s.png'
				if self.death_type == 'goo':
					path = 'protagonist/goo' + str((int(render_counter // 3) % 4) + 1) + '.png'
				
			elif self.standingon == None:
				path = 'protagonist/fall' + str((int(render_counter // 3) % 4) + 1) + '.png'
			else:
				dir = self.last_direction_of_movement
				if self.pushing != None:
					dir = self.pushing.lower() + 'push'
				path = 'protagonist/' + dir
				if self.spray_counter >= 0:
					path += 'spray' + str(((render_counter // 3) % 4) + 1)
				elif self.is_moving:
					path += str([1, 2, 3, 4, 3, 2][(render_counter // 6) % 6])
				path += '.png'
			img = get_image(path)
		elif self.isjanitor:
			if self.holding_spray:
				path = 'janitor/spray2.png'
			elif self.holding_walkie:
				path = 'janitor/walkietalkie2.png'
			else:
				dir = self.last_direction_of_movement
				if dir == 's' or dir == 'n':
					dir += 'e'
				elif dir == 'e' or dir == 'w':
					dir = 's' + dir
				path = 'janitor/' + dir
				if self.is_moving:
					path += str([1, 2, 3, 4, 3, 2][(render_counter // 6) % 6])
				path += '.png'
			img = get_image(path)
		elif self.issupervisor:
			dir = self.last_direction_of_movement
			#TODO: get n, s, e, w images of supervisor|janitor
			if dir == 's' or dir == 'n':
				dir += 'e'
			elif dir == 'e' or dir == 'w':
				dir = 's' + dir
			path = 'supervisor/' + dir
			if self.is_moving:
				path += str([1, 2, 3, 4, 3, 2][(render_counter // 6) % 6])
			path += '.png'
			img = get_image(path)
		elif self.staticy:
			img = get_image('static/character' + str(((render_counter // 6) % 4) + 1) + '.png')
		elif self.isblock:
			img = self.block_tile.get_image(render_counter)

		return img
	
	def pixel_position(self, xOffset, yOffset, img):
		x = self.x - self.y
		y = (self.x + self.y) / 2
		if img == None:
			w = 16
			h = 32
		else:
			w = img.get_width()
			h = img.get_height()
		x = x - w / 2
		y = y - self.z - h + 8
		if self.isblock:
			y += 8
		
		if self.ismain or self.staticy:
			if self.staticy and self.ttype.startswith('block|'):
				y += 16
			y += 8

		platform = self.standingon
		if platform != None and platform.stairs:
			left = platform.topography[3] * 8
			right = platform.topography[1] * 8
			if platform.entrance == 'SW' or platform.entrance == 'NE':
				ap = self.y % 16 + 0.0
				p = 16.0 - ap
			else:
				p = self.x % 16 + 0.0
				ap = 16.0 - p
			dy = int((left * ap + p * right) / 16.0)
			y -= dy
			
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
		
	
	def get_replacement_sprite(self):
		if self.trecv and self.garbage_collect:
			self.prototype.garbage_collect = False
			return self.prototype
		return self
	
	def update(self, level):
		self.death_counter -= 1
		self.spray_counter -= 1
		
		if self.death_counter == 1:
			self.garbage_collect = True
		
		if self.automation != None:
			auto_xy = self.automation.get_next_values()
			self.dx += auto_xy[0]
			self.dy += auto_xy[1]
		
		self.pushing = None
		self.falling = False
		if self.ttl != None:
			self.ttl -= 1
			if self.ttl <= 0:
				self.garbage_collect = True
				if self.trecv:
					self.prototype.x = self.x
					self.prototype.y = self.y
					self.prototype.z = self.z
					self.prototype.is_moving = False
					self.prototype.immobilized = False
		
		if self.immobilized:
			return
		if self.standingon == None:
			self.dz = -1

		if self.dz != 0:
			platform_data = level.get_platform_below(int(self.x) // 16, int(self.y) // 16, self.z, True)
			if platform_data != None:
				z = platform_data[0]
				platform = platform_data[1]
				if z < self.dz + self.z:
					self.z += self.dz
					self.falling = True
				else:
					self.z = z
					self.standingon = platform
			else:
				self.standingon = None
				self.z += self.dz
		layer = self.z // 8
		on_new_coordinates_now = False
		new_platform = self.standingon
		
		starting_col = int(self.x) // 16
		starting_row = int(self.y) // 16
		
		if self.standingon != None:
			if self.standingon.teleporter and not self.staticy:
				destination = level.teleporters.get_destination(starting_col, starting_row, int(self.z // 8) - 1)
				
				if destination != None:
					if destination == 'blocked':
						pass
						# TODO: play blocked sound
					else:
						level.teleporters.teleport_sprite(self, destination)
		
		if self.dz == 0:
			
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
									
									self.pushing = direction
									
									if push_key == prev_push_target:
										level.push_counter -= 1
									else:
										level.push_counter = level.max_push_counter
									if level.push_counter == 0:
										# Try to do the push
										if tcol >= 0 and tcol < level.width and trow >= 0 and trow < level.height:
											tlookup = level.cellLookup[tcol][trow]
											tstack = level.grid[tcol][trow]
											bottom_free = True
											top_free = True
											bottom_index = c + layer - 1
											top_index = c + layer
											
											if len(tlookup) > bottom_index:
												bottom_index = tlookup[bottom_index]
												if bottom_index != None:
													if tstack[bottom_index].blocking or tstack[bottom_index].cant_push_over:
														bottom_free = False
											
											if len(tlookup) > top_index:
												top_index = tlookup[top_index]
												if top_index != None:
													if tstack[top_index].blocking or tstack[top_index].cant_push_over:
														top_free = False
											
											if bottom_free and top_free:
												# TODO: make sure you're not pushing onto a ramp
												target_level = c + layer - 1
												while len(tlookup) <= target_level:
													tstack.append(None)
													tlookup.append(None)
												_t = tlookup[target_level - 1]
												_i = target_level - 1
												while _i >= 0 and _t == None:
													_t = tlookup[_i]
													_i -= 1
												
												if _i == -1:
													_t = -1
												
												valid = True
												while _t >= 0:
													landing_tile = tstack[_t]
													
													if landing_tile != None:
														if landing_tile.stairs:
															valid = False
														elif landing_tile.no_blocks:
															valid = False
														else:
															valid = True
														break
													_t -= 1
												
												if valid:
													level.push_block(col, row, tcol, trow, target_level)
												else:
													level.push_counter = -1
													level.push_target = None
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
				old_col = int(self.x // 16)
				old_row = int(self.y // 16)
				self.x += self.dx
				self.y += self.dy
				new_col = int(self.x // 16)
				new_row = int(self.y // 16)
				if old_col != new_col or old_row != new_row:
					on_new_coordinates_now = True
				
				new_layer = int(self.z // 8)
				
				occupying = level.get_tile_at(new_col, new_row, new_layer)
				if occupying != None and occupying.is_goo and self.main_or_hologram:
					self.death_counter = 60
					self.death_type = 'goo'
					self.immobilized = True
					
			
			if self.automation == None:
				omg_hax = self.dx != 0 and self.dy != 0
			else:
				omg_hax = self.dx != 0 or self.dy != 0
			
			if omg_hax:
				distance = (self.dx * self.dx + self.dy * self.dy) ** .5
				ndx = self.dx / distance
				ndy = self.dy / distance
				
				tolerance = .35
				dy_off = ndy > -tolerance and ndy < tolerance
				dx_off = ndx < tolerance and ndx > -tolerance
				
				d = None
				self.is_moving = True
				
				if dx_off:
					if dy_off:
						pass
					elif ndy < 0:
						d = 'ne'
					else:
						d = 'sw'
				elif ndx < 0:
					if dy_off:
						d = 'nw'
					elif ndy < 0:
						d = 'n'
					else:
						d = 'w'
				else:
					if dy_off:
						d = 'se'
					elif ndy < 0:
						d = 'e'
					else:
						d = 's'
				if d != None:
					self.last_direction_of_movement = d
					self.direction_queue = [d] + self.direction_queue[:4]
					if len(self.direction_queue) == 5:
						a,b,c,d,e = self.direction_queue
						if len(a) == 1 and d == e and len(d) == len(e) and a in d and ((b == c and (b == a or b == d)) or (b == a and c == d)): # BWAHAHAHAHAHA
							self.last_direction_of_movement = d
				
			else:
				self.is_moving = False
			
		if new_platform != None and new_platform.stairs and on_new_coordinates_now:
			if direction == new_platform.entrance:
				self.z -= new_platform.height * 8
		
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
		
		if self.ismain:
			self.try_pick_up_powerups(level)
	
	def try_pick_up_powerups(self, level):
		col = int(self.x // 16)
		row = int(self.y // 16)
		layer = int(self.z // 8)
		if layer < 0: return
		tile = level.get_tile_at(col, row, layer)
		if tile != None and tile.powerup:
			play_sound('pickup.wav')
			level.modify_block(col, row, layer, None)
			if tile.goo:
				increment_persisted_level_int('decontaminant', tile.goo_size)
			else:
				increment_persisted_level_int('research', 1)
				