class ClickyButton:
	def __init__(self, id, x, y, text, on_color, off_color, pressed_color, action, get_label):
		self.id = id
		self.text = text
		self.on_color = on_color
		self.off_color = off_color
		self.pressed_color = pressed_color
		self.pressed = False
		self.on_color = on_color
		self.off_color = off_color
		self.pressed_color = pressed_color
		self.left = x
		self.top = y
		size = 14
		self.size = size
		self.enabled = True
		if text != None:
			self.on_img = get_text(text, size, on_color)
			self.off_img = get_text(text, size, off_color)
			self.pressed_img = get_text(text, size, pressed_color)
			self.right = x + self.off_img.width
			self.bottom = y + self.off_img.height
		else:
			self.right = x + 10
			self.bottom = y + get_text("!y", size, 'black').height
		self.im = get_input_manager()
		self.action = action
		self.get_label = get_label
		self.last_text = None
	
	def is_mouse_over(self):
		x, y = self.im.get_cursor_position()
		if self.left > x or self.right < x or self.top > y or self.bottom < y:
			return False
		return True
	
	def is_pressing(self):
		return self.is_mouse_over() and self.im.get_mouse_status()
		
	def render(self, screen):
		if self.get_label != None:
			label = self.get_label(self.id)
			if label == '---': # horrible hack
				self.enabled = False
			else:
				self.enabled = True
			if label != self.last_text:
				self.pressed_img = get_text(label, self.size, self.pressed_color)
				self.on_img = get_text(label, self.size, self.on_color)
				self.off_img = get_text(label, self.size, self.off_color)
				self.bottom = self.on_img.height + self.top
				self.right = self.on_img.width + self.left
		
		if not self.enabled:
			img = self.off_img
		elif self.is_pressing():
			img = self.pressed_img
		elif self.is_mouse_over():
			img = self.on_img
		else:
			img = self.off_img
		
		img.draw(self.left, self.top)
	
	def on_click(self):
		if self.enabled:
			self.action(self.id)

class ConfigureInputScene:
	def __init__(self):
		self.next = self
		hb = self.handle_button
		a = (255, 255, 0)
		b = (255, 255, 255)
		c = (128, 128, 255)
		self.labels = []
		heading = (200, 200, 200)
		heading_size = 20
		command_color = (128, 180, 255)
		key_command_color = (255, 255, 255)
		use_mouse_label_size = 18
		
		js_option_y_coords = []
		self.key_command_color = key_command_color
		use_mouse_label = get_text("Use the mouse for this screen", use_mouse_label_size, (100, 255, 100))
		self.use_mouse_label = use_mouse_label
		
		js_label = get_text("Select Active Joystick", heading_size, heading)
		self.labels.append(((10, 10), js_label))
		y = 10 + 10 + js_label.height
		x = 20
		js_option_y_coords.append(y)
		
		self.buttons = [ClickyButton('no joystick', x, y, "None", a, b, c, hb, None)]
		self.buttons.append(ClickyButton('exit', 300, 5, "Return to Main Menu", a, b, c, hb, None))
		im = get_input_manager()
		i = 1
		self.im = im
		for js in im.actual_joysticks:
			y += 20
			js_option_y_coords.append(y)
			self.buttons.append(ClickyButton('joystick ' + str(i), x, y, js.get_name(), a, b, c, hb, None))
			i += 1
		
		self.js_option_coords = js_option_y_coords
		
		y += 30
		gl = self.get_button_label
		self.labels.append(((10, y), get_text("Commands", heading_size, heading)))
		y += 20
		col1 = 20
		col2 = 115
		col3 = 205
		self.js_config_x = col3
		self.js_config_y = []
		self.keys = [
			None,
			('left', "Left", "Left Arrow"),
			('right', "Right", "Right Arrow"),
			('up', "Up", "Up Arrow"),
			('down', "Down", "Down Arrow"),
			('start', "Pause/Confirm", "Enter"),
			('spray', "Decontaminant", "Space"),
			('walkie', "Walkie Talkie", "W"),
			(None, "Quit", 'Esc / Alt+F4')]
		for command in self.keys:
			
			start_y = y
			self.js_config_y.append(y)
			if command == None:
				self.labels.append(((col2, y), get_text("Key", 14, heading)))
				self.labels.append(((col3, y), get_text("Joystick", 14, heading)))
			else:
				self.labels.append(((col1, y), get_text(command[1], 14, command_color)))
				if command[0] == None:
					self.labels.append(((col2, y), get_text(command[2], 14, key_command_color)))
				else:
					self.buttons.append(ClickyButton('keyconfig ' + command[0], col2, y, None, a, b, c, hb, gl))
					self.buttons.append(ClickyButton('jsconfig ' + command[0], col3, y, None, a, b, c, hb, gl))
			y += 16
	
	def get_button_label(self, id):
		parts = id.split(' ')
		if parts[0] == 'jsconfig':
			return self.im.get_config_label_for_key_for_active(parts[1])
		elif parts[0] == 'keyconfig':
			return self.im.get_config_label_for_key_for_keyboard(parts[1])
				
		return " "
	
	def save_changes(self):
		im = get_input_manager()
		im.save_config()
		im.save_key_config()
	
	def handle_button(self, id):
		im = get_input_manager()
		if id == 'exit':
			self.save_changes()
			self.next = TransitionScene(self, MainMenuScene())
		elif id == 'no joystick':
			im.set_active_actual_joystick(-1)
		else:
			parts = id.split(' ')
			if parts[0] == 'joystick':
				im.set_active_actual_joystick(int(parts[1]) - 1)
			elif parts[0] == 'keyconfig':
				action = parts[1]
				self.next = SetInputScene(action, True, self)
			elif parts[0] == 'jsconfig':
				action = parts[1]
				self.next = SetInputScene(action, False, self)
			else:
				self.next = TransitionScene(MainMenuScene(), self)
	
	def process_input(self, events, pressed, axes, mouse):
		for mouse_event in mouse:
			if mouse_event[2] == False and mouse_event[3] == False:
				for button in self.buttons:
					if button.is_mouse_over():
						button.on_click()
						break
		
	def update(self, counter):
		pass
	
	def render(self, screen, counter):
		im = get_input_manager()
		
		for button in self.buttons:
			button.render(screen)
		for label in self.labels:
			
		
			pos = label[0]
			img = label[1]
			img.draw(pos[0], pos[1])
		
		if ((counter // 25) % 2) == 1:
			self.use_mouse_label.draw(
				200 - self.use_mouse_label.width // 2,
				300 - self.use_mouse_label.height)
		
		if im.active_actual_joystick == -1:
			i = 0
		else:
			i = im.active_actual_joystick + 1
		x = 5
		y = self.js_option_coords[i]
		Graphics2D.Draw.rectangle(x, y + 2, 4, 4, 255, 0, 0)
