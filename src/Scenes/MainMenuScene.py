class MainMenuScene:
	def __init__(self):
		self.next = self
		self.index = 0
		self.first = True
		has_save_data = get_persisted_forever_string('save_level') != ''
		self.options = [
			('Start New Story Mode', True, lambda x:PlayScene('intro', True)),
			('Resume Saved Game', has_save_data, 'resume_save'),
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
					if self.index < len(self.options) and not self.options[self.index][1]:
						self.index += 1
					if self.index < len(self.options):
						play_sound('menumove')
					else:
						self.index = len(self.options) - 1
				elif event.key == 'up':
					self.index -= 1
					if not self.options[self.index][1]:
						self.index -= 1
					
					if self.index >= 0:
						play_sound('menumove')
					else:
						self.index == 0
				elif event.key == 'start':
					go = True
		
		self.index = max(self.index, 0)
		self.index = min(self.index, len(self.options) - 1)
		
		if go:
			lamb = self.options[self.index][2]
			if lamb == 'resume_save':
				level = get_persistent_state().get_string_forever('save_level')
				next_scene = PlayScene(level, True)
			else:
				next_scene = lamb(None)
			self.next = TransitionScene(self, next_scene)
	
	def update(self, counter):
		get_jukebox().ensure_current_song('title')
		if self.first:
			self.first = False
			get_persistent_state().session = {}
	
	def render(self, screen, counter):
		get_image('misc/title_screen.png').draw(0, 0)
		
		title = get_text("Sudo Science", 36, (255, 255, 255))
		w = title.width
		h = title.height
		title.draw(20, 20)
		
		y = h + 30 + 20
		i = 0
		for option in self.options:
			x = 20
			color = (190, 190, 190)
			if self.index == i:
				Graphics2D.Draw.rectangle(x, y + 5, 5, 5, 255, 255, 255)
			elif not option[1]:
				color = (80, 80, 80)
			x = 30
			text = get_text(option[0], 18, color)
			text.draw(x, y)
			y += text.height + 10
			i += 1
