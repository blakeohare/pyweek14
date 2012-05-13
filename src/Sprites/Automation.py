class Automation:
	def __init__(self, level, type):
		self.type = type
		self.level = level
		self.counter = 0
		self.intro_dialog_start = 329 + 14
	
	# (dx, dy)
	def get_next_values(self):
		c = self.counter
		sprite = self.sprite
		self.counter += 1
		o = None
		if self.level == '99-0':
			o = self.do_99_player(self.level, c, sprite)
		else:
			if self.type == 'intro_janitor':
				o = self.do_intro_janitor(self.level, c, sprite)
			elif self.type == 'intro_supervisor':
				o = self.do_intro_supervisor(self.level, c, sprite)
			elif self.type == 'intro_protagonist':
				o = self.do_intro_protagonist(self.level, c, sprite)
			if o == None:
				return (0, 0)
		return o
	
	def do_99_player(self, level, counter, sprite):
		
		if counter < 15:
			return (0, 0)
		elif counter < 23:
			return (-1.5, 0)
		elif counter < 40:
			return (0, 1.5)
		elif counter < 57:
			return (0, -1.5)
		elif counter < 69:
			return (-1.5, 0)
		elif counter == 80:
			
			
			drf2 = get_tile_store().get_tile('drf2')
			sprite.level.modify_block(4, 4, 1, drf2)
		return (0, 0)

	def hold_spray(self, sprite):
		sprite.holding_spray = True
	def unhold_spray(self, sprite):
		sprite.holding_spray= False
	def hold_walkie(self, sprite):
		sprite.holding_walkie = True
	def unhold_walkie(self, sprite):
		sprite.holding_walkie = False
	def kill_me(self, sprite):
		sprite.garbage_collect = True
	
	def do_intro_janitor(self, level, counter, sprite):
		#print counter
		
		
		
		ranges = [
		# less than, then return, and do...
		(8, (1, 2)),
		(116, (0, 2)),
		(4, (-2, 0)),
		(182, (0, 0)),
		(4, (-1, 0)),
		(40, (0, 0), self.hold_spray),
		(1, (0, 0), self.unhold_spray),
		(6, (0, 0)),
		(4, (1, 0)),
		(1, (-1, 0)),
		(210, (0, 0)),
		(4, (-1, 0)),
		(6, (0, 0)),
		(40, (0, 0), self.hold_walkie),
		(26, (0, 0), self.unhold_walkie),
		(6, (1, 0)),
		(1, (-1, 0)),
		(30, (0, 0)),
		(4, (1, 0)),
		(40, (0, 1.4)),
		(1, (0, 0), self.kill_me),
		(999, (0, -4))
		]
		cumulative = 0
		for r in ranges:
			cumulative += r[0]
			if counter < cumulative:
				if len(r) == 3:
					r[2](sprite)
				#print 'jan', counter, r
				return r[1]
		
			
	
	def do_intro_supervisor(self, level, counter, sprite):
		
		
		ranges = [
		# less than, then return, and do...
		(8, (1, 2)),
		(108, (0, 2)),
		(4, (-2, 0)),
		(320, (0, 0)),
		(4, (1, 0)),
		(60, (0, 1)),
		(1, (0, 0), self.kill_me),
		(999, (0, -4))
		]
		cumulative = 0
		for r in ranges:
			cumulative += r[0]
			if counter < cumulative:
				if len(r) == 3:
					r[2](sprite)
				
				return r[1]
		
		
		
		leave_begin = 373
		if counter < 116:
			if counter < 8:
				x = 1
			else:
				x = 0
			return (x, 2)
		elif counter < 120:
			return (-2, 0)
		
		elif counter > leave_begin:
			t = leave_begin
			if counter < t + 16:
				return (1, 0)
			elif counter < t + 16 + 48:
				return (0, 1)
			elif counter == 450:
				sprite.garbage_collect = True
	
	def do_intro_protagonist(self, level, counter, sprite):
		s = 180
		if counter == s + 132:
			sprite.intro_hack = True
			level.modify_block(int(sprite.x // 16), int(sprite.y // 16), int(sprite.z // 8), get_tile_store().get_tile('54'))
		if counter < s + 132:
			return None
		if counter < s + 148:
			return (0, 1)
		if counter < s + 149:
			return (1, 0)
