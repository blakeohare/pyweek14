class PlayScene:
	def __init__(self, level_name):
		self.next = self
		self.level_name = level_name
		self.level = Level(level_name)
		self.player = Sprite(17, 177, 32, 'main')
		self.sprites = [self.player]
		self.overlay = PlaySceneOverlay(self, self.level)
	def process_input(self, events, pressed, axes):
		if not self.player.immobilized:
			dx = axes[0]
			dy = axes[1]
			self.player.dx = dx
			self.player.dy = dy
	
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
		
		self.overlay.render(screen, counter)