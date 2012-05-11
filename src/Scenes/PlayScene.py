class PlayScene:
	def __init__(self, level_name):
		self.next = self
		self.level_name = level_name
		self.level = Level(level_name)
		self.player = Sprite(17, 177, 32, 'main')
		self.sprites = [self.player]
		for rat in self.level.rats:
			rat.z = 8 * 8
			rat.standingon = None
			self.sprites.append(rat)
		self.overlay = PlaySceneOverlay(self, self.level)
		self.do_not_override_start = False
		level_manager = get_level_manager()
		self.counter = 0
		start = level_manager.get_starting_point_for_level(level_name)
		self.do_stuff = get_hacks_for_level(level_name, 'do_stuff')
		
		if start != None:
			x = start[0]
			y = start[1]
			z = start[2]
			dir = 's'
			if len(start) >= 4:
				dir = start[3]
			self.do_not_override_start = True
		
			self.player.x = x * 16 + 8
			self.player.y = y * 16 + 8
			self.player.z = z * 8
			self.player.last_direction_of_movement = dir
			self.player.standingon = self.level.get_tile_at(x, y, z - 1)
		
		level_pixel_width = self.level.height * 16 + self.level.width * 16
		level_pixel_height = level_pixel_width // 2 + 12 * 8
		self.fixed_x = level_pixel_width < 400
		self.fixed_y = level_pixel_height < 300
		self.target_camera_x = None
		self.target_camera_y = None
		self.camera_x = None
		self.camera_y = None
		if self.do_stuff != None:
			self.do_stuff(self, self.level, -1)
	
	def process_input(self, events, pressed, axes, mouse):
		for event in events:
			if event.key == 'spray' and event.down and self.player.spray_counter < 0:
				if get_persisted_level_int('decontaminant') > 0:
					self.player.spray_counter = 30
					self.level.spray_from(self.player)
					play_sound('spray.wav')
					increment_persisted_level_int('decontaminant', -1)
			
		
		if not self.player.immobilized and self.player.automation == None:
			dx = axes[0]
			dy = axes[1]
			if self.player.spray_counter < 0:
				self.player.dx = dx
				self.player.dy = dy
		
		
	
	def update(self, counter):
		level = self.level
		player = self.player
		
		if self.do_stuff != None:
			self.do_stuff(self, level, self.counter)
		
		if player.death_by_rat > 0:
			player.death_by_rat += 1
			if player.death_by_rat == 90:
				self.restart_level()
		
		filtered = []
		for sprite in self.sprites:
			sprite.update(level)
			sprite = sprite.get_replacement_sprite()
			if not sprite.garbage_collect:
				filtered.append(sprite)
			
			if sprite.israt and not player.death_by_rat:
				dx = sprite.x - player.x
				dy = sprite.y - player.y
				distance = dx * dx + dy * dy
				print distance
				if distance < 256:
					player.death_by_rat = 1
					player.immobilized = True
		
		
		
		self.sprites = filtered + level.get_new_sprites()
		
		if self.player.death_counter == 1:
			self.restart_level()
		
		if self.player.z < -140:
			self.restart_level()
		
		self.counter += 1
	
	def restart_level(self):
		self.next = TransitionScene(self, PlayScene(self.level.name))
	
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