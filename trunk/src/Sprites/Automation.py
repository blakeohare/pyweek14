class Automation:
	def __init__(self, level, type):
		self.type = type
		self.level = level
		self.counter = 0
	
	# (dx, dy)
	def get_next_values(self):
		c = self.counter
		self.counter += 1
		o = None
		if self.type == 'intro_janitor':
			o = self.do_intro_janitor(self.level, c)
		elif self.type == 'intro_supervisor':
			o = self.do_intro_supervisor(self.level, c)
		elif self.type == 'intro_protagonist':
			o = self.do_intro_protagonist(self.level, c)
		if o == None:
			return (0, 0)
		return o
	
	def do_intro_janitor(self, level, counter):
		if counter < 116:
			return (0, 2)
		if counter == 116:
			return (-1, 0)
	
	def do_intro_supervisor(self, level, counter):
		if counter < 124:
			return (0, 2)
		if counter == 124:
			return (-1, 0)
	
	def do_intro_protagonist(self, level, counter):
		s = 180
		if counter < s + 132:
			return None
		if counter < s + 148:
			return (0, 1)
		if counter < s + 149:
			return (1, 0)