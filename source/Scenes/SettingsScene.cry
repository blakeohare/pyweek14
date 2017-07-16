# Sound* settings
class SettingsScene:
	def __init__(self):
		self.next = self
		self.i = 0
		self.jk = get_jukebox()
	
	def toggle_magic(self):
		z = 1 - get_persisted_forever_int('magic')
		set_persisted_forever_int('magic', z)
	
	def process_input(self, events, pressed, axes, mouse):
		for event in events:
			if event.down:
				if event.key == 'up':
					self.i -= 1
					if self.i == -1:
						self.i = 0
					else:
						play_sound('menumove')
				if event.key == 'down':
					self.i += 1
					if self.i > 3:
						self.i = 3
					else:
						play_sound('menumove')
				
				if event.key == 'right':
					if self.i == 0: # SFX
						self.jk.set_sfx_volume(self.jk.get_sfx_volume() + 10)
						play_sound('menumove')
					elif self.i == 1: # Music
						self.jk.set_music_volume(self.jk.get_music_volume() + 10)
						play_sound('menumove')
					elif self.i == 2:
						self.toggle_magic()
						play_sound('menumove')
				
				elif event.key == 'left':
					if self.i == 0: # SFX
						self.jk.set_sfx_volume(self.jk.get_sfx_volume() - 10)
						play_sound('menumove')
					elif self.i == 1: # Music
						self.jk.set_music_volume(self.jk.get_music_volume() - 10)
						play_sound('menumove')
					elif self.i == 2:
						self.toggle_magic()
						play_sound('menumove')
				
				elif event.key == 'start':
					if self.i == 2:
						self.toggle_magic()
						play_sound('menumove')
					elif self.i == 3:
						get_persistent_state().set_int_forever('sfx', self.jk.get_sfx_volume())
						get_persistent_state().set_int_forever('music', self.jk.get_music_volume())
						self.next = TransitionScene(self, MainMenuScene())
						get_persistent_state().save_game()
						play_sound('menumove')
						
				
					
	
	def update(self, counter):
		pass
		
	
	def render(self, screen, counter):
		header = get_text("Sound Settings", 30, (255, 255, 255))
		x = (GAME_WIDTH - header.width) // 2
		y = 30
		header.draw(x, y)
		
		y += header.height + 30
		
		g = (120, 120, 120)
		w = (255, 255, 255)
		
		c = w if self.i == 0 else g
		img = get_text("SFX Volume: " + str(self.jk.get_sfx_volume()) + "%", 18, c)
		img.draw((GAME_WIDTH - img.width) // 2, y)
		y += img.height + 40
		
		c = w if self.i == 1 else g
		img = get_text("Music Volume: " + str(self.jk.get_music_volume()) + "%", 18, c)
		img.draw((GAME_WIDTH - img.width) // 2, y)
		y += img.height + 40
		
		c = w if self.i == 2 else g
		t = "More Magic " if (get_persisted_forever_int('magic') == 1) else "Magic"
		img = get_text(t, 18, c)
		img.draw((GAME_WIDTH - img.width) // 2, y)
		y += img.height + 40
		
		c = w if self.i == 3 else g
		img = get_text("Return to Main Menu", 18, c)
		img.draw((GAME_WIDTH - img.width) // 2, y)
		y += img.height + 40
		
		
		