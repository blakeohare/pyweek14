_dark_overlay = None

class PauseScene:
	def __init__(self, playscene):
		global _dark_overlay
		self.next = self
		self.playscene = playscene
		if _dark_overlay == None:
			_dark_overlay = pygame.Surface((400, 300)).convert()
			_dark_overlay.fill((0, 0, 0))
			_dark_overlay.set_alpha(180)
		self.overlay = _dark_overlay
		self.i = 0
		self.options = [
			"Continue",
			"Restart Level",
			"Use Walkie Talkie (Save Game)",
			"Main Menu",
			"Quit"]
		
	
	def process_input(self, events, pressed, axes, mouse):
		for event in events:
			if event.down:
				if event.key == 'up':
					self.i -= 1
					if self.i < 0:
						self.i = 0
					else:
						play_sound('menu_move')
				elif event.key == 'down':
					self.i += 1
					if self.i < len(self.options):
						play_sound('menu_move')
				elif event.key == 'spray' or event.key == 'start':
					self.do_it()
		if self.i < 0:
			self.i = 0
		if self.i >= len(self.options):
			self.i = len(self.options) - 1
		
	def do_it(self):
		i = max(0, min(len(self.options) - 1, self.i))
		if i == 0:
			# Continue
			self.next = self.playscene
			self.next.next = self.next
		elif i == 1:
			self.next = TransitionScene(self, PlayScene(self.playscene.level.name, self.playscene.story_mode, True))
		elif i == 2:
			self.save_game()
			self.next = DialogScene(self.playscene, 'save')
		elif i == 3:
			self.next = TransitionScene(self, MainMenuScene())
		elif i == 4:
			self.next = None
	
	def save_game(self):
		get_persistent_state().set_string_forever('save_level', self.playscene.level.name)
		get_persistent_state().save_game()
	def update(self, counter):
		pass
	
	def render(self, screen, counter):
		self.playscene.render(screen, counter)
		screen.blit(self.overlay, (0, 0))
		y = 100
		
		i = 0
		for option in self.options:
			text = self.options[i]
			color = (100, 100, 100)
			if self.i == i:
				color = (255, 255, 255)
			img = get_text(text, 18, color)
			
			x = screen.get_width() // 2 - img.get_width() // 2
			screen.blit(img, (x, y))
			i += 1
			y += img.get_height() + 20