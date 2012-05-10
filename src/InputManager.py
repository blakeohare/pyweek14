
class MyEvent:
	def __init__(self, key, down):
		self.key = key
		self.down = down
		self.up = not down

_input_manager = None

def get_input_manager():
	global _input_manager
	if _input_manager == None:
		_input_manager = InputManager()
	return _input_manager

class InputManager:
	def __init__(self):
		self.joysticks = []
		self.active_joystick = -1
		self.read_config_save()
		self.activate_joysticks()
		self.active_actual_joystick = -1
		self.events = []
		self.quitAttempt = False
		self._key_mapping = {
			pygame.K_RETURN: 'start',
			pygame.K_LEFT: 'left',
			pygame.K_RIGHT: 'right',
			pygame.K_UP: 'up',
			pygame.K_DOWN: 'down',
			pygame.K_SPACE: 'spray',
			pygame.K_w: 'walkie'
		}
		self.my_pressed = {
			'start': False,
			'left': False,
			'right': False,
			'up': False,
			'down': False,
			'spray': False,
			'walkie': False
		}
		
		self.axes = [0.0, 0.0]
	
	def get_events(self):
		events = []
		keyboard_only = True
		self.axes = [0.0, 0.0]
		pg_pressed = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type in (pygame.KEYDOWN, pygame.KEYUP):
				down = event.type == pygame.KEYDOWN
				if down and event.key == pygame.K_F4:
					if pg_pressed[pygame.K_LALT] or pg_pressed[pygame.K_RALT]:
						self.quitAttempt = True
						return []
				elif down and event.key == pygame.K_ESCAPE:
					self.quitAttempt = True
					return []
				
				action = self._key_mapping.get(event.key, None)
				
				if action != None:
					self.my_pressed[action] = down
					events.append(MyEvent(action, down))
		self.axes[0] = 2.0 if self.my_pressed['right'] else 0.0
		self.axes[0] = -2.0 if self.my_pressed['left'] else self.axes[0]
		self.axes[1] = 2.0 if self.my_pressed['down'] else 0.0
		self.axes[1] = -2.0 if self.my_pressed['up'] else self.axes[1]

		joystick = None
		config = None
		any_axes_found = False
		if self.active_joystick != -1:
			config = self.joysticks[self.active_joystick]
			name = config.get('name', '')
			for js in self.actual_joysticks:
				name2 = js.get_name()
				if name.lower() == name2.lower():
					joystick = js
					break
		
		if joystick != None and config != None:
			cached_poll = {}
			for action in ('right', 'left', 'up', 'down', 'start', 'spray', 'walkie'):
				direction = False
				c = config.get(action, None)
				x = False
				if c != None:
					n = c[1]
					if c[0] == 'axis':
						direction = True
						x = cached_poll.get('a' + str(n))
						if x == None:
							x = joystick.get_axis(n)
							if abs(x) < 0.01:
								x = 0
							cached_poll['a' + str(n)] = x
						
						if c[2][1] == '+':
							if x < 0:
								x = 0
						else:
							if x > 0:
								x = 0
							else:
								x *= -1
						x = abs(x)
						
						if x > 0.01:
							keyboard_only = False
							if not any_axes_found:
								any_axes_found = True
								self.axes = [0.0, 0.0]
						
					elif c[0] == 'hat':
						direction = True
						x = cached_poll.get('h' + str(n))
						if x == None:
							x = joystick.get_hat(n)
							cached_poll['h' + str(n)] = x
						if c[2][0] == 'x':
							x = x[0]
						else:
							x = x[1]
						
						if c[2][1] == '+':
							if x < 0:
								x = 0
						else:
							if x > 0:
								x = 0
							else:
								x *= -1
						x = abs(x)
					elif c[0] == 'button':
						x = cached_poll.get('b' + str(n))
						if x == None:
							x = joystick.get_button(n)
							cached_poll['b' + str(n)] = x
						
					
					if action in ('start', 'spray', 'walkie'):
						pushed = x
						if direction:
							pushed = x >= .5
						if self.my_pressed[action] != pushed:
							self.my_pressed[action] = pushed
							events.append(MyEvent(action, pushed))
					elif action in ('left', 'right', 'down', 'up'):
						
						toggled = False
						if direction:
							pushed = x + 0.0
						else:
							pushed = 0.0 if (pushed < .5) else 1.0
						toggled = pushed > .2
						if pushed < 0.01:
							pushed = 0
						
						if toggled != self.my_pressed[action]:
							self.my_pressed[action] = toggled
							events.append(MyEvent(action, toggled))
						
						if action == 'left':
							if abs(self.axes[0]) < 0.01 and pushed > 0.01:
								self.axes[0] = -2 * pushed
						
						elif action == 'right':
							if abs(self.axes[0]) < 0.01 and pushed > 0.01:
								self.axes[0] = 2 * pushed
								
						elif action == 'up':
							if abs(self.axes[1]) < 0.01 and pushed > 0.01:
								self.axes[1] = -2 * pushed
								
						elif action == 'down':
							if abs(self.axes[1]) < 0.01 and pushed > 0.01:
								self.axes[1] = 2 * pushed
		
		self.axes[0] = self.axes[0] / 1.8
		
		x = self.axes[0]
		y = self.axes[1]
		
		if not any_axes_found and x != 0 and y != 0:
			xsign = 1 if (x > 0) else -1
			ysign = 1 if (y > 0) else -1
			x = 1.2 * xsign
			y = 1.2 * ysign
			
		if abs(x) < 0.05 and abs(y) < 0.05:
			rx = 0.0
			ry = 0.0
			
		else:
			ang = 3.14159265 / 4.0
			c = math.cos(ang)
			s = math.sin(ang)
			rx = x * c + y * s
			ry = -x * s + y * c
		
		self.axes[0] = rx
		self.axes[1] = ry
		
		return events
			
	def activate_joysticks(self):
		self.actual_joysticks = []
		active_joystick_name = None
		if self.active_joystick != -1:
			active_joystick_name = self.joysticks[self.active_joystick].get('name')
		for i in range(pygame.joystick.get_count()):
			js = pygame.joystick.Joystick(i)
			js.init()
			self.actual_joysticks.append(js)
			name = trim(js.get_name())
			
	def verify_axis_value(self, x):
		return len(x) == 2 and x[0] in 'xy' and x[1] in '-+'
	
	def save_config(self):
		output = []
		if self.active_joystick != -1 and self.active_joystick < len(self.joysticks):
			output.append('#active: ' + self.joysticks[self.active_joystick].get('name', ''))
		else:
			output.append('#active: ')
		for joystick in self.joysticks:
			output.append(self._save_joystick(joystick))
		output = '$'.join(output)
		write_file('data/input_config.txt', output)
		
	def _save_joystick(self, config):
		output = []
		for key in config.keys():
			value = ' '.join(safe_map(str, config[key]))
			row = '#' + key + ': ' + value
			output.append(row)
			
		return '\n'.join(output)
	
	def read_config_save(self):
		prev = read_file('data/input_config.txt')
		if prev != None:
			data = trim(prev).split('$')
			if len(data) > 0:
				active = trim(data[0])
				parts = active.split(':')
				active_joystick_name = None
				if len(parts) >= 2 and trim(parts[0]) == '#active':
					active_joystick_name = trim(':'.join(parts[1:]))
				for config in data[1:]:
					lines = config.split('\n')
					data = {}
					for line in lines:
						line = trim(line)
						if len(line) > 0 and line[0] == '#':
							parts = line[1:].split(':')
							if len(parts) == 2:
								key = trim(parts[0])
								value = trim(parts[1]).split(' ')
								if value[0] == 'axis':
									if len(value) == 3:
										n = parseInt(value[1])
										if self.verify_axis_value(value[2]):
											data[key] = ('axis', n, value[2])
								elif value[0] == 'button':
									if len(value) == 2:
										n = parseInt(value[1])
										data[key] = ('button', n)
								elif value[0] == 'hat':
									if len(value) == 3:
										n = parseInt(value[1])
										if self.verify_axis_value(value[2]):
											data[key] = ('hat', n, value[2])
								elif key == 'name':
									data[key] = trim(' '.join(value))
					name = data.get('name', None)
					if name != None and len(name) > 0:
						if active_joystick_name != None and active_joystick_name.lower() == name.lower():
							self.active_joystick = len(self.joysticks)
						self.joysticks.append(data)
	