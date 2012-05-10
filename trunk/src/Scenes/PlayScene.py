class PlayScene:
	def __init__(self, level_name):
		self.next = self
		self.level_name = level_name
		self.level = Level(level_name)
		self.player = Sprite(17, 177, 32, 'main')
		self.sprites = [self.player]
		self.overlay = PlaySceneOverlay(self, self.level)
		
		level_pixel_width = self.level.height * 16 + self.level.width * 16
		level_pixel_height = level_pixel_width // 2 + 12 * 8
		self.fixed_x = level_pixel_width < 400
		self.fixed_y = level_pixel_height < 300
		self.target_camera_x = None
		self.target_camera_y = None
		self.camera_x = None
		self.camera_y = None
		
	def process_input(self, events, pressed, axes, mouse):
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
		
		player_position = self.player.pixel_position(0, 0, None)
		player_x = player_position[0]
		player_y = player_position[1]
		
		if self.fixed_x:
			self.target_camera_x = screen.get_width() // 2
		else:
			self.target_camera_x = screen.get_width() // 2 - player_x
		
		if self.fixed_y:
			self.target_camera_y = 50
		else:
			self.target_camera_y = 120 - player_y
		
		if self.camera_x == None:
			self.camera_x = self.target_camera_x
		if self.camera_y == None:
			self.camera_y = self.target_camera_y
		
		max_pan_speed = 4
		if self.camera_x != self.target_camera_x:
			if abs(self.camera_x - self.target_camera_x) == 1:
				self.camera_x = self.target_camera_x
			else:
				new_camera_x = (self.camera_x + self.target_camera_x) // 2
				if abs(new_camera_x - self.camera_x) > max_pan_speed:
					if self.camera_x < new_camera_x:
						self.camera_x += max_pan_speed
					else:
						self.camera_x -= max_pan_speed
				else:
					self.camera_x = new_camera_x
		
		if self.camera_y != self.target_camera_y:
			if abs(self.camera_y - self.target_camera_y) == 1:
				self.camera_y = self.target_camera_y
			else:
				new_camera_y = (self.camera_y + self.target_camera_y) // 2
				if abs(new_camera_y - self.camera_y) > max_pan_speed:
					if self.camera_y < new_camera_y:
						self.camera_y += max_pan_speed
					else:
						self.camera_y -= max_pan_speed
				else:
					self.camera_y = new_camera_y
		
		self.level.render(screen, self.camera_x, self.camera_y, self.sprites, counter, sprites_to_add, sprites_to_remove)
		for sprite in sprites_to_remove:
			sprite.garbage_collect = True
		for sprite in sprites_to_add:
			self.sprites.append(sprite)
		
		self.overlay.render(screen, counter)