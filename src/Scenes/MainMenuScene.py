class MainMenuScene:
	def __init__(self):
		self.next = self
		self.index = 0
		has_save_data = get_persisted_forever_int('has_save_data') == 1
		self.options = [
			('Start New Story Mode', True, lambda x:PlayScene('intro', True)),
			('Resume Saved Game', has_save_data, lambda x:PlayScene(None, True)),
			('Level Picker', True, lambda x:LevelPickerScene()),
			('Configure Input', True, lambda x:ConfigureInputScene()),
			('Sound Settings', True, lambda x:SettingsScene()),
			('Credits', True, lambda x:CreditsScene(True)),
			('Exit', True, lambda x:GoodbyeScene())
			]

	def process_input(self, events, pressed, axes, mouse):
		go = False
		for event in events:
			if event.down:
				if event.key == 'down':
					self.index += 1
					if not self.options[self.index][1]:
						self.index += 1
				elif event.key == 'up':
					self.index -= 1
					if not self.options[self.index][1]:
						self.index -= 1
				elif event.key == 'start':
					go = True
		
		self.index = max(self.index, 0)
		self.index = min(self.index, len(self.options) - 1)
		
		if go:
			next_scene = self.options[self.index][2](None)
			self.next = TransitionScene(self, next_scene)
	
	def update(self, counter):
		pass
	
	def render(self, screen, counter):
		title = get_text("Sudo Scientific", 36, (255, 255, 255))
		w = title.get_width()
		h = title.get_height()
		screen.blit(title, (screen.get_width() // 2 - w // 2, 30))
		
		y = h + 30 + 20
		i = 0
		for option in self.options:
			x = 100
			color = (190, 190, 190)
			if self.index == i:
				color = (255, 255, 255)
				pygame.draw.rect(screen, color, pygame.Rect(x, y + 5, 5, 5))
			elif not option[1]:
				color = (80, 80, 80)
			x = 110
			text = get_text(option[0], 18, color)
			screen.blit(text, (x, y))
			y += text.get_height() + 10
			i += 1