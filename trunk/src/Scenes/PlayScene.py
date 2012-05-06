class PlayScene:
	def __init__(self, level_name):
		self.next = self
		self.level_name = level_name
		self.level = Level(level_name)
		
	def process_input(self, events, pressed):
		pass
	
	def update(self, counter):
		pass
	
	def render(self, screen, counter):
		self.level.render(screen, screen.get_width() / 2, 50, counter)
		