class GoodbyeScene:
	def __init__(self):
		self.next = self
		
	def process_input(self, events, pressed, axes, mouse):
		for event in events:
			self.next = None
	
	def update(self, counter):
		pass
	
	def render(self, screen, counter):
		bye = get_text("Goodbye", 16, (255, 255, 255))
		x = (screen.get_width() - bye.get_width()) // 2
		y = (screen.get_height() - bye.get_height()) // 2
		screen.blit(bye, (x, y))
		
		img = get_image('protagonist/wave' + str(((counter // 3) % 4) + 1) + '.png')
		
		screen.blit(img, (192, y + 20))
		