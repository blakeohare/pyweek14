class TransitionScene:
	def __init__(self, before, after):
		self.next = self
		self.before = before
		self.after = after
		self.counter = 0
		self.blackness = None
		
	def process_input(self, events, pressed, axes):
		pass
	
	def update(self, counter):
		self.counter += 1
		if self.counter >= 60:
			self.next = self.after
		
	def render(self, screen, counter):
		
		if self.counter <= 30:
			opacity = 255 * self.counter // 30
			bg = self.before
		else:
			opacity = (60 - self.counter) * 255 // 30
			bg = self.after
		
		if self.blackness == None:
			self.blackness = pygame.Surface((screen.get_width(), screen.get_height())).convert()
			self.blackness.fill((0, 0, 0))
		
		bg.render(screen, counter)
		self.blackness.set_alpha(opacity)
		screen.blit(self.blackness, (0, 0))