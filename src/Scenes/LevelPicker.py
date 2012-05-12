_level_image = {}


class LevelPickerScene:
	def __init__(self):
		self.next = self
		self.x = 0
		self.y = 0
		self.regions = [
			("Sector A", '1-3 2-3 2a-0 3-1'.split()),
			("Sector B", '4-0 5-0 6-0 7-0'.split()),
			("Sector C", '8-0 9-0 10-2 11-0'.split()),
			("Sector D", '12-0 13-0 14-0 14a-0'.split()),
			("Sector E", '15-0 16-0 17-3 18-0'.split()),
			("Sector F", '19a-0 19b-1'.split()),
			("Sector G", '19-0 20-0 21-0'.split()),
			("Sector H", 'flipmaze 25-0'.split()),
			("Sector I", '24-0'.split()),
			("Sector J", '26-0 27-0 28-0'.split()),
			("Sector X", '90-0'.split())
		]
		
	def get_level_image(self, name):
		global _level_image
		img = _level_image.get(name)
		if img == None:
			img = get_image('levelshots/' + name + '.png')
			w = img.get_width()
			h = img.get_height()
			if w > 100:
				h = h * 100 // w
				w = 100
			if h > 60:
				w = w * 60 // h
				h = 60
			img = pygame.transform.scale(img, (w, h))
			_level_image[name] = img
		return img
		
	def process_input(self, events, pressed, axes, mouse):
		for event in events:
			if event.down:
				if event.key == 'left':
					self.x -= 1
					if self.x < 0:
						self.x = 0
					else:
						play_sound('menumove')
						self.y = 0
				elif event.key == 'right':
					self.x += 1
					if self.x > len(self.regions):
						self.x = len(self.regions) - 1
					else:
						play_sound('menumove')
						self.y = 0
				
				elif event.key == 'down':
					self.y += 1
					if self.y >= len(self.regions[self.x][1]):
						self.y -= 1
					else:
						play_sound('menumove')
				elif event.key == 'up':
					self.y -= 1
					if self.y < 0:
						self.y = 0
					else:
						play_sound('menumove')
					
				elif event.key == 'start':
					if self.x == len(self.regions):
						self.next = TransitionScene(self, MainMenuScene())
					else:
						self.next = TransitionScene(self, PlayScene(self.regions[self.x][1][self.y], False))
				
	
	def update(self, counter):
		pass
	
	def render(self, screen, counter):
		screen.fill((48, 48, 48))
		bye = get_text("Level Picker", 18, (255, 255, 255))
		x = (screen.get_width() - bye.get_width()) // 2
		screen.blit(bye, (x, 10))
		
		x = 10
		y = 30
		i = 0
		sector = get_text("Sector: ", 16, (255, 255, 0))
		screen.blit(sector, (x, y))
		
		x += sector.get_width() + 10
		for region in self.regions + [None]:
			
			color = (130, 130, 130)
			if i == self.x:
				color = (255, 255, 255)
			if region == None:
				label = get_text("Main Menu", 16, color)
			else:
				label = get_text(self.regions[i][0].split(' ')[1], 16, color)
			screen.blit(label, (x, y))
			x += label.get_width() + 10
			i += 1
		
		y += sector.get_height() + 10
		
		if self.x < len(self.regions):
			lm = get_level_manager()
			i = 0
			maps = self.regions[self.x][1]
			for m in maps:
				img = self.get_level_image(m)
				screen.blit(img, (30, y))
				
				color = (120, 120, 120)
				if self.y == i:
					color = (255, 255, 255)
				name_label = get_text(lm.get_current_room_name(m), 20, color)
				screen.blit(name_label, (150, y))
				y += 60
				i += 1