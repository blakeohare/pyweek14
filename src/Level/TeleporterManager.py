class TeleporterManager:
	def __init__(self, level):
		self.level = level
		transporters = level.get_teleporters()
		self.counter = 0
		senders = []
		receivers = []
		enabled = []
		in_use = []
		if len(transporters) == 2:
			for t in transporters:
				if t[3] == 't1' or t[3] == 't3':
					senders.append(t)
					enabled.append(t[3] == 't1')
				else:
					receivers.append(t)
		else:
			pass
			# TODO: configure it for when there are multiple
			# currently, it'll be in the order of the parser
		self.senders = senders
		self.receivers = receivers
		self.new_sprites = {}
		self.remove_sprites = []
		self.in_use = len(self.senders) * [999]
		self.enabled = enabled
		
	
	def set_teleporter_status(self, col, row, layer, isenabled):
		i = 0
		total = len(self.senders)
		while i < total:
			sender = self.senders[i]
			if sender[0] == col and sender[1] == row and sender[2] == layer:
				enabled[i] = isenabled
				self.update_tiles(i)
				return
			receiver = self.receivers[i]
			if receiver[0] == col and receiver[1] == row and receiver[2] == layer:
				enabled[i] = isenabled
				self.update_tiles(i)
				return
	
	def enable_teleporter(self, col, row, layer):
		self.set_teleporter_status(col, row, layer, True)
	
	def disable_teleporter(self, col, row, layer):
		self.set_teleporter_status(col, row, layer, False)
	
	def update_tiles(self, index):
		sender = self.senders[index]
		receiver = self.receivers[index]
		level = self.level
		ts = get_tile_store()
		s_tile = ts.get_tile('t1')
		r_tile = ts.get_tile('t2')
		if not self.enabled[index]:
			s_tile = ts.get_tile('t3')
			r_tile = ts.get_tile('t3')
		level.modify_block(sender[0], sender[1], sender[2], s_tile)
		level.modify_block(receiver[0], receiver[1], receiver[2], r_tile)
	
	def get_destination(self, col, row, layer):
		final = self.get_sender((col, row, layer))
		if final != None and self.enabled[final]:
			output = self.receivers[final]
			for i in range(4):
				z = output[2] + i + 1
				tile = self.level.get_tile_at(output[0], output[1], z)
				if tile != None and tile.blocking:
					return 'blocked'
			if self.in_use[final] < 200:
				return None
			self.in_use[final] = 0
			return output
		return None

	def teleport_block(self, blocktype, source, target):
		
		sprite = Sprite(source[0] * 16 + 8, source[1] * 16 + 8, source[2] * 8, 'block|'+blocktype.id)
		self.teleport_sprite(sprite, target)
	
	def teleport_sprite(self, sprite, target):
		sprite.immobilized = True
		self.remove_sprites.append(sprite)
		
		self.new_sprites[self.counter + 1] = self.new_sprites.get(self.counter + 1, [])
		self.new_sprites[self.counter + 1].append(Sprite(sprite.x, sprite.y, sprite.z, 'teleport|' + sprite.type))
		
		self.new_sprites[self.counter + 120] = self.new_sprites.get(self.counter + 120, [])
		z = (target[2] + 1) * 8
		clone = Sprite(target[0] * 16 + 8, target[1] * 16 + 8, z, 'receiving|' + sprite.type)
		clone.standingon = get_tile_store().get_tile('t2')
		clone.prototype = sprite
		
		self.new_sprites[self.counter + 120].append(clone)
	
	def tag_as_in_use(self, coords):
		sender_index = self.get_sender(coords)
		if sender_index != None:
			self.in_use[sender_index] = 0
			
	def is_in_use(self, i):
		return self.in_use[i] <= 90
	
	def get_sender(self, coords):
		i = 0
		while i < len(self.senders):
			s = self.senders[i]
			if s[0] == coords[0] and s[1] == coords[1] and s[2] == coords[2]:
				return i
			i += 1
		return None
	
	def get_new_sprites(self):
		new_sprites = self.new_sprites.get(self.counter, None)
		if new_sprites == None:
			return []
		return self.new_sprites.pop(self.counter)
		
	
	def get_removed_sprites(self):
		output = self.remove_sprites
		self.remove_sprites = []
		return output
	
	def update(self):
		self.counter += 1
		i = 0
		while i < len(self.in_use):
			self.in_use[i] += 1
			i += 1
	