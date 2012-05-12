class CreditsScene:
	def __init__(self, canSkip):
		self.next = self
		self.canSkip = canSkip
		self.speed = .7
		self.counter = 0
		self.things = [
		[None, (' ', "Credits"), None],
		[None, ("Programming", "Blake O'Hare"), 'blake'],
		['spears', ("Level Art", "Angel McLaughlin"), None],
		[None, ("Music and Sound", "Adrian Cline"), 'ikanreed'],
		['satyrane', ("Story and Dialog", "Laura Freer"), None],
		[None, ("Portrait and Large Art", "\"Fixception\""), 'fixception'],
		['brendan', ("Puzzle Design", "Brendan & Steve"), 'stiva'],
		['duke', ("Level Implementation", "Will Duke & Ted Burton"), 'eofpi'],
		[None, (" ", "Thank you for playing."), None]
		]
		
		if not self.canSkip:
			r = get_persisted_forever_int('research')
			r += get_persisted_session_int('research')
			self.things.append(
			[None, (" ", "Research papers collected: " + str(r) + " out of 35"), None]
			)
		
		i = 0
		while i < len(self.things):
			thing = self.things[i]
			left = thing[0]
			right = thing[2]
			if left != None:
				left = get_image('us/' + left + '.png')
			if right != None:
				right = get_image('us/' + right + '.png')
				right = pygame.transform.flip(right, True, False)
			self.things[i][0] = left
			self.things[i][2] = right
			
			i += 1
		
	def process_input(self, events, pressed, axes, mouse):
		for event in events:
			if event.down:
				if event.key == 'start' or event.key == 'spray' or event.key == 'walkie':
					if self.canskip:
						self.next = TransitionScene(self, MainMenuScene())
	
	def update(self, counter):
		get_jukebox().ensure_current_song('stringtheory')
		self.counter += 1
	
	def render(self, screen, counter):
		
		y = 350 - int(self.counter * self.speed)# * 1.4)
		
		for item in self.things:
			left = item[0]
			right = item[2]
			top = get_text(item[1][0], 14, (123, 123, 123))
			bottom = get_text(item[1][1], 24, (255, 255, 255))
			
			x1 = screen.get_width() // 2 - top.get_width() // 2
			x2 = screen.get_width() // 2 - bottom.get_width() // 2
			x = min(x1, x2)
			screen.blit(top, (x1, y))
			y2 = y + top.get_height() + 5
			screen.blit(bottom, (x2, y2))
			r = 400 - x
			if left != None:
				screen.blit(left, (x - left.get_width() - 14, y - 5))
			if right != None:
				screen.blit(right, (r + 14, y - 5))
			y = y2 + bottom.get_height() + 140
		
		if y < -50:
			self.next = TransitionScene(self, MainMenuScene())