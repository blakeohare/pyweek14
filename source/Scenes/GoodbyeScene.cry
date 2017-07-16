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
		x = (GAME_WIDTH - bye.width) // 2
		y = (GAME_HEIGHT - bye.height) // 2
		bye.draw(x, y)
		
		img = get_image('protagonist/wave' + str(((counter // 3) % 4) + 1) + '.png')
		
		img.draw(192, y + 20)
		