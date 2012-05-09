class CreditsScene:
	def __init__(self, canSkip):
		self.next = self
		self.canSkip = canSkip
		
	def process_input(self, events, pressed):
		for event in events:
			self.next = None
	
	def update(self, counter):
		pass
	
	def render(self, screen, counter):
		bye = get_text("Credits", 16, (255, 255, 255))
		x = (screen.get_width() - bye.get_width()) // 2
		y = (screen.get_height() - bye.get_height()) // 2
		screen.blit(bye, (x, y))
		