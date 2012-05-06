class TitleScene:
	def __init__(self):
		self.next = self
		self.text = get_text(
			"If you can read this, then you are",
			24, (255, 255, 0))
		self.textb = get_text(
			"100% set up to use Python + PyGame",
			24, (255, 255, 0))
		self.x = 0
		self.y = 0

	def process_input(self, events, pressed):
		pass
	
	def update(self, counter):
		self.x += 1
		self.y += 2
	
	def render(self, screen, counter):
		w = screen.get_width()
		h = screen.get_height()
		self.x = (self.x + w) % w
		self.y = (self.y + h) % h
		
		for t in ((0, 0), (-1, 0), (0, -1), (-1, -1)):
			x = self.x + w * t[0]
			y = self.y + h * t[1]
			screen.blit(self.text, (x, y))
			screen.blit(self.textb, (x, y + self.textb.get_height() + 4))
			