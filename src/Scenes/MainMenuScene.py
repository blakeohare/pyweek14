class MainMenuScene:
	def __init__(self):
		self.next = self
		self.index = 0
		self.options = [
			('Play Game', lambda x:PlayScene('intro')),
			('Configure Input', lambda x:ConfigureInputScene()),
			('Credits', lambda x:CreditsScene(True)),
			('Exit', lambda x:GoodbyeScene())
			]

	def process_input(self, events, pressed, axes):
		go = False
		for event in events:
			if event.down:
				if event.key == 'down':
					self.index += 1
				elif event.key == 'up':
					self.index -= 1
				elif event.key == 'start':
					go = True
		
		self.index = max(self.index, 0)
		self.index = min(self.index, len(self.options) - 1)
		
		if go:
			next_scene = self.options[self.index][1](None)
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
			x = 110
			text = get_text(option[0], 18, color)
			screen.blit(text, (x, y))
			y += text.get_height() + 10
			i += 1