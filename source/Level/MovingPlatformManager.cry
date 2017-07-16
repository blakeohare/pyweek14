class MovingPlatformManager:
	
	def __init__(self, level):
		self.level = level
		self.ticker = 0
		self.pause_tokens = {}
		self.initialize_pause_tokens(level.name)
		
		directions = get_hacks_for_level(level.name, 'moving_platforms')
		if directions == None:
			directions = []
		else:
			directions = safe_map(lambda x:x.split(), directions)
		self.platforms = self.level.get_moving_platforms()
		self.num_platforms = len(self.platforms)
		while len(directions) < self.num_platforms:
			directions.append(['P'])
		self.directions = directions
	
	def set_pause_token(self, i, on):
		self.pause_tokens[str(i)] = on
	
	def initialize_pause_tokens(self, name):
		pt = self.pause_tokens
		if name == '16-0':
			pt['0'] = True
		elif name == '18-0':
			for i in range(0, 11):
				pt[str(i)] = True
		elif name == '24-0':
			pt['2'] = True
		elif name == '25-0':
			for i in range(9):
				pt[str(i)] = True
		elif name == '90-0':
			pt['0'] = True
	
	def is_paused_platform(self, i):
		if self.pause_tokens.get(str(i)) == True:
			return True
		return False
	
	def update(self, sprites, render_exceptions):
		self.ticker += 1
		if self.ticker % 60 == 0:
			level = self.level
			i = 0
			while i < self.num_platforms:
				
				if not self.is_paused_platform(i):
				
					platform = self.platforms[i]
					directions = self.directions[i]
					direction = directions[0]
					if direction == 'P':
						directions.pop(0)
						directions.append('P')
					else:
						target = [platform[0], platform[1], platform[2]]
						
						if direction == 'NW':
							target[0] -= 1
							offset = (-1, 0)
						elif direction == 'NE':
							target[1] -= 1
							offset = (0, -1)
						elif direction == 'SW':
							target[1] += 1
							offset = (0, 1)
						else:
							target[0] += 1
							offset = (1, 0)
						t_lower = level.get_tile_at(target[0], target[1], target[2])
						t_upper = level.get_tile_at(target[0], target[1], target[2] + 1)
						if t_lower == None and t_upper == None:
							move_us = [platform]
							
							z = move_us[-1][2] + 2
							col = platform[0]
							row = platform[1]
							lookupStack = level.cellLookup[col][row]
							stack = level.grid[col][row]
							spritification = []
							while z < len(lookupStack):
								if lookupStack[z] != None:
									tile = stack[lookupStack[z]]
									if tile != None:
										if tile.pushable:
											
											neighbor_lookup = level.cellLookup[col + offset[0]][row + offset[1]]
											neighbor_stack = level.grid[col + offset[0]][row + offset[1]]
											blocked = False
											if len(spritification) == 0:
												for z_offset in (z + 0, z + 1):
													if len(neighbor_lookup) <= z_offset:
														pass
													else:
														
														if z_offset < 0:
															ntile = None
														else:
															ntile = neighbor_lookup[z_offset]
														if ntile != None:
															ntile = neighbor_stack[ntile]
															if ntile != None and ntile.blocking:
																blocked = True
																break
											else:
												blocked = True
											loc = [col, row, z]
											if blocked:
												spritification.append(loc)
											else:
												move_us.append(loc)
												
											z += tile.height - 1
										else:
											break
									else:
										break
								else:
									break
								z += 1
							
							for block in spritification:
								level.spritify_block(block[0], block[1], block[2])
							
							first = True
							for move_me in move_us:
								mp = level.modify_block(move_me[0], move_me[1], move_me[2], None)
								target = [move_me[0] + offset[0], move_me[1] + offset[1], move_me[2]]
								level.modify_block(target[0], target[1], target[2], mp)
								
								if first:
									self.platforms[i] = target
								render_exceptions.append(RenderException(move_me, direction, mp, True))
								first = False
							directions.append(directions.pop(0))
							
							
							for sprite in sprites:
								if sprite.standingon != None and Math.floor(sprite.x // 16) == move_us[-1][0] and Math.floor(sprite.y // 16) == move_us[-1][1] and Math.floor(sprite.z // 8) == move_us[-1][2] + 2:
									sx = Math.floor(sprite.x // 16)
									if sx == move_us[-1][0]:
										sy = Math.floor(sprite.y // 16)
										sz = Math.floor(sprite.z // 8)
										if sy == move_us[-1][1] and sz == move_us[-1][2] + 2:
											coords = (Math.floor(sprite.x // 16), Math.floor(sprite.y // 16), Math.floor(sprite.z // 8))
											target = [coords[0] + offset[0], coords[1] + offset[1], coords[2]]
											lookup = level.cellLookup[target[0]][target[1]]
											stack = level.grid[target[0]][target[1]]
											blocked = False
											for _i in range(sprite.height):
												check = [target[0], target[1], target[2] + _i]
												t = level.get_tile_at(check)
												if t != None and t.blocking:
													blocked = True
											if not blocked:
												render_exceptions.append(RenderException(coords, direction, sprite, False))
												sprite.x += offset[0] * 16
												sprite.y += offset[1] * 16
											else:
												sprite.standingon = None
							
				i += 1

