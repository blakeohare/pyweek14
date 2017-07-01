_set_input_shade = None

def get_set_input_shade():
	global _set_input_shade
	if _set_input_shade == None:
		_set_input_shade = pygame.Surface((400, 300)).convert()
		_set_input_shade.fill((0, 0, 0))
		_set_input_shade.set_alpha(170)
	return _set_input_shade
	
class SetInputScene:
	def __init__(self, action, is_keyboard, prev_scene):
		self.next = self
		self.prev = prev_scene
		self.is_keyboard = is_keyboard
		self.action = action
		font_size = 20
		self.tryanother = get_text("Key in use, try another", 12, (255, 0, 0))
		self.show_tryanother = False
		font_color = (255, 255, 255)
		self.counter = 0
		if self.is_keyboard:
			self.top_img = get_text("Press the key on the keyboard", font_size, font_color)
		else:
			self.top_img = get_text("Press the button on the gamepad", font_size, font_color)
		self.bottom_img = get_text('that will be used to ' +{
			'left': "move left",
			'right': 'move right',
			'up': 'move up',
			'down': 'move down',
			'start': 'pause or confirm menus',
			'spray': 'spray decontaminant',
			'walkie': 'use your walkie talkie (save)'
		}[action], font_size, font_color)
		
	
	def key_in_use(self, code, action):
		km = get_input_manager()._key_mapping
		for k in km.keys():
			if k == code:
				if km[k] != action:
					self.show_tryanother = True
					return True
				else:
					return False
		return False
	
	def leave(self):
		self.next = self.prev
		self.prev.next = self.prev
		
	def process_input(self, events, pressed, axes, mouse):
		im = get_input_manager()
		
		if self.is_keyboard:
			for ku in im.raw_keyups:
				if not self.key_in_use(ku, self.action):
					im.set_key_config(self.action, ku)
					self.leave()
					break
		else:
			# TODO: disable button to get here if self.active_actual_joystick is -1
			js = im.actual_joysticks[im.active_actual_joystick]
			js_config = im.joysticks[im.active_joystick]
			for i in range(js.get_numbuttons()):
				if js.get_button(i):
					js_config[self.action] = ('button', i)
					self.leave()
					return
			for i in range(js.get_numaxes()):
				value = js.get_axis(i)
				if Math.abs(value) > .3:
					sign = '+' if (value > 0) else '-'
					js_config[self.action] = ('axis', i, 'x' + sign)
					self.leave()
					return
			
			for i in range(js.get_numhats()):
				value = js.get_hat(i)
				if value[0] != 0 or value[1] != 0:
					axis = 'x' if (value[1] == 0) else 'y'
					value = value[0] if (axis == 'x') else value[1]
					sign = '+' if (value > 0) else '-'
					js_config[self.action] = ('hat', i, axis + sign)
					self.leave()
					return
	
	def update(self, counter):
		self.counter
	
	def render(self, screen, counter):
		self.prev.render(screen, counter)
		get_set_input_shade().draw(0, 0)
		if self.is_keyboard:
			label = "Press the key on the keyboard"
		else:
			label = "Press the button on the gamepad"
		h = self.top_img.height
		y = 150 - h - 3
		left = 25
		top = y - 20
		width = 350
		height = h * 2 + 6 + 40
		Graphics2D.Draw.rectangle(left, top, width, height, 128, 128, 128)
		Graphics2D.Draw.rectangle(left + 1, top + 1, width - 2, height - 2, 0, 0, 0)
		self.top_img.draw(200 - self.top_img.width // 2, y)
		self.bottom_img.draw(200 - self.bottom_img.width // 2, 150 + 3)
		if self.show_tryanother:
			self.tryanother.draw(200 - self.tryanother.width // 2, top + height - 15)
