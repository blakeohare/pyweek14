class MovingPlatformManager:
	
	def __init__(self, level):
		self.level = level
		self.ticker = 0
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
			
	def update(self, sprites, render_exceptions):
		self.ticker += 1
		if self.ticker % 60 == 0:
			level = self.level
			i = 0
			while i < self.num_platforms:
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
						
						while z < len(lookupStack):
							if lookupStack[z] != None:
								tile = stack[lookupStack[z]]
								if tile != None:
									if tile.pushable:
										
										
										if True:# TODO: check for impediments
											move_us.append([col, row, z])
											
										z += tile.height - 1
									else:
										break
								else:
									break
							else:
								break
							z += 1
						
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
							if sprite.standingon != None and int(sprite.x // 16) == move_us[-1][0] and int(sprite.y // 16) == move_us[-1][1] and int(sprite.z // 8) == move_us[-1][2] + 2:
								sx = int(sprite.x // 16)
								if sx == move_us[-1][0]:
									sy = int(sprite.y // 16)
									sz = int(sprite.z // 8)
									if sy == move_us[-1][1] and sz == move_us[-1][2] + 2:
										coords = (int(sprite.x // 16), int(sprite.y // 16), int(sprite.z // 8))
										render_exceptions.append(RenderException(coords, direction, sprite, False))
										sprite.x += offset[0] * 16
										sprite.y += offset[1] * 16
						
				i += 1

