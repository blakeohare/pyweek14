class HologramManager:
	def __init__(self, level):
		self.level = level
		pads = level.get_hologram_pads()
		self.copy_pad = None
		self.output_pads = []
		for pad in pads:
			if pad[3]:
				self.copy_pad = pad
			else:
				self.output_pads.append(pad)
		
		self.copy_mode_counter = -1
		self.used = False
		self.new_sprites = []
		self.sprites_created = []
		
	def get_new_sprites(self):
		ns = self.new_sprites
		self.new_sprites = []
		return ns
	
	def animation_sequence(self):
		if self.copy_mode_counter < 0:
			return None
		else:
			copy_process = self.copy_mode_counter > 0
			for sprite in self.sprites_created:
				sprite.clone_creating = copy_process
		return self.copy_mode_counter
	
	def update(self, playscene, level, player):
		if self.copy_pad == None: return
		
		self.copy_mode_counter -= 1
		if self.used:
			return
		
		cp = self.copy_pad
		
		col = Math.floor(player.x // 16)
		row = Math.floor(player.y // 16)
		layer = Math.floor(player.z // 8) - 1
		
		if cp[0] == col and cp[1] == row and cp[2] == layer:
			self.copy_mode_counter = 180
			# TODO: add new sprites
			self.used = True
			player.x = col * 16 + 8
			player.y = row * 16 + 8
			for p in self.output_pads:
				pc = p[0]
				pr = p[1]
				pl = p[2] + 1
				self.new_sprites.append(Sprite(pc * 16 + 8, pr * 16 + 8, pl * 8, 'hologram|main'))
				if level.name == '26-0' and playscene.story_mode:
					playscene.next = DialogScene(playscene, 'hologram')
			self.sprites_created = self.new_sprites[:]