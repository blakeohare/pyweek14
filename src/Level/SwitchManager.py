_switch_mapping = {
	'4-0': [
		'blue'
	],
	
	'5-0': [
		'bridge',
		None,
		None
	],
	
	'8-0': [
		'exit'
	],
	
	'9-0': [
		'exit'
	],
	
	'10-2': [
		'bridgene',
		'bridgenw',
		'bridgese'
	],
	
	'12-0': [
		'exit'
	],
	
	'14-0': [
		'blue',
		'exit'
	],
	
	'16-0': [
		None,
		'green'
	],
	
	'17-3': [
		'red',
		'blue'
	],
	
	'18-0': [None] * 9,
	
	'19-0': [
		'power'
	],
	
	'20-0': [
		'blue',
		'power'
	]
}

def override_switch_behavior(manager, level, index):
	enabled = manager.enabled
	name = level.name
	
	if name == '5-0':
		if index > 0:
			if enabled[1] and enabled[2]:
				level.activate_switch('door', True)
			else:
				level.activate_switch('door', False)
				
			return True
	
	elif name == '16-0':
		if index == 0:
			# Don't confuse the meaning of these 0's.
			# The index == 0 which is the switch ID
			# The pause token is 0 which is the moving platform ID
			# They're the same here because that's a coincidence
			level.moving_platforms.set_pause_token('0', not enabled[index])
			return True
	
	elif name == '18-0':
		mapping = [
			[10],
			[0],
			[2],
			[4],
			[1, 9],
			[5],
			[7],
			[8],
			[3, 6]
		]
		for platform in mapping[index]:
			level.moving_platforms.set_pause_token(str(platform), not enabled[index])
		return True
	return False


class SwitchManager:
	def __init__(self, level):
		#self.playscene = playscene
		self.level = level
		self.switches = self.level.get_switches()
		self.enabled = [False] * len(self.switches)
		self.statuses = [None] * len(self.switches)
		self.locations = {}
		for switch in self.switches:
			k = str(switch[0]) + '^' + str(switch[1])
			self.locations[k] = self.locations.get(k, [])
			self.locations[k].append(switch)
		
		ts = get_tile_store()
		self.rubiks = ts.get_tile('rubiks')
		self.colors = {
			# Switch, block
			'gray': (ts.get_tile('b1'), ts.get_tile('3')),
			'red': (ts.get_tile('b2'), ts.get_tile('9')),
			'blue': (ts.get_tile('b4'), ts.get_tile('10')),
			'green': (ts.get_tile('b3'), ts.get_tile('11')),
			'magenta': (ts.get_tile('b6'), ts.get_tile('12')),
			'cyan': (ts.get_tile('b5'), ts.get_tile('13')),
			'yellow': (ts.get_tile('b7'), ts.get_tile('14')),
			'battery': (ts.get_tile('pi'), ts.get_tile('45')),
		}
		
		self.activator_lookup = {}
		for color in self.colors.keys():
			self.activator_lookup[self.colors[color][0].id] = self.colors[color][1]
		
	
	def update_statuses_for_sprite(self, sprite, level):
		col = int(sprite.x // 16)
		row = int(sprite.y // 16)
		layer = int(sprite.z // 8) - 1
		
		floor = level.get_tile_at(col, row, layer)
		if floor != None and floor.isswitch:
			i = 0
			while i < len(self.switches):
				sw = self.switches[i]
				
				if sw[0] == col and sw[1] == row and sw[2] == layer:
					self.statuses[i] = ('sprite', sprite)
					break
				i += 1
	
	def check_switch_for_block_and_update(self, i, switch, level):
		col = switch[0]
		row = switch[1]
		layer = switch[2] + 1
		above = level.get_tile_at(col, row, layer)
		if above != None and above.pushable:
			self.statuses[i] = ('block', above)
		
		
	def update_statuses(self, sprites):
		if len(self.switches) == 0:
			return
		
		i = 0
		while i < len(self.switches):
			self.statuses[i] = None
			i += 1
		
		players = []
		level = self.level
		for sprite in sprites:
			if sprite.main_or_hologram:
				players.append(sprite)
			else:
				self.update_statuses_for_sprite(sprite, level)
		for p in players:
			self.update_statuses_for_sprite(p, level)
		
		i = 0
		while i < len(self.switches):
			self.check_switch_for_block_and_update(i, self.switches[i], level)
			i += 1
		
	def update_enabled(self, sprites, suppress_triggers):
		
		self.update_statuses(sprites)
		before = self.enabled[:]
		
		i = 0
		while i < len(self.switches):
			switch = self.switches[i]
			status = self.statuses[i]
			if status != None:
				if status[0] == 'sprite':
					if switch[3] == self.colors['gray'][0]:
						self.enabled[i] = True
				elif status[0] == 'block':
					type = switch[3]
					if type == self.colors['gray'] or status[1] == self.rubiks:
						self.enabled[i] = True
					elif self.activator_lookup[type.id] == status[1]:
						self.enabled[i] = True
					else:
						self.enabled[i] = False
			else:
				self.enabled[i] = False
			
			if not suppress_triggers:
				if before[i] != self.enabled[i]:
					self.do_action(self.level, self.level.name, i, self.enabled[i])
					
			
			i += 1
		
	def do_action(self, level, name, switch_index, positive):
		global _switch_mapping
		
		if override_switch_behavior(self, level, switch_index):
			return
		
		mapping = _switch_mapping.get(name)
		if mapping != None:
			action_name = mapping[switch_index]
			level.activate_switch(action_name, positive)
		#print "Level", name, switch_index, positive
		#pass
		