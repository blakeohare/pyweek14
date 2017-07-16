class TransitionScene:
	def __init__(self, before, after):
		self.next = self
		self.before = before
		self.after = after
		self.counter = 0
		
	def process_input(self, events, pressed, axes, mouse):
		pass
	
	def update(self, counter):
		self.counter += 1
		if self.counter >= 60:
			self.next = self.after
		
	def render(self, screen, counter):
		
		if self.counter <= 30:
			opacity = self.counter / 30.0
			bg = self.before
		else:
			opacity = (60 - self.counter) / 30.0
			bg = self.after
		
		alpha = Math.floor(opacity * 255)
		if (alpha > 255): alpha = 255
		elif (alpha < 0): alpha = 0
		
		bg.render(screen, counter)
		Graphics2D.Draw.rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, 0, 0, 0, alpha)
