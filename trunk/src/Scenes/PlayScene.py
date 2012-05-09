class PlayScene:
	def __init__(self, level_name):
		self.next = self
		self.level_name = level_name
		self.level = Level(level_name)
		self.player = Sprite(17, 177, 32, 'main')
		self.sprites = [self.player]
		# axis values are +/- 0, 1, 2, or 3
		self.v = [0, 0.5, 1, 1.5]
		self.v += safe_map(lambda x:-x, self.v[1:][::-1])

	def process_input(self, events, pressed):
		if not self.player.immobilized:
			dx = pressed['x-axis']
			dy = pressed['y-axis']
			self.player.dx = self.v[dx]
			self.player.dy = self.v[dy]
	
	def update(self, counter):
		level = self.level
		filtered = []
		for sprite in self.sprites:
			sprite.update(level)
			sprite = sprite.get_replacement_sprite()
			if not sprite.garbage_collect:
				filtered.append(sprite)
		self.sprites = filtered + level.get_new_sprites()
	
	def render(self, screen, counter):
		sprites_to_add = []
		sprites_to_remove = []
		self.level.render(screen, screen.get_width() / 2, 50, self.sprites, counter, sprites_to_add, sprites_to_remove)
		for sprite in sprites_to_remove:
			sprite.garbage_collect = True
		for sprite in sprites_to_add:
			self.sprites.append(sprite)
		