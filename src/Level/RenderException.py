_render_exceptions_coords = [
(2, 1), # 7
(4, 2), # 6
(6, 3), # 5
(8, 4), # 4
(10, 5), # 3
(12, 6), # 2
(14, 7), # 1
]

class RenderException:
	
	# start is a set of 3D coordinates
	def __init__(self, start, direction, tile):
		global _render_exceptions_coords
		self.z = start[2]
		self.counter = 0
		self.expired = False
		if direction == 'NE' or direction == 'NW':
			self.do_show = start
			if direction == 'NE':
				self.dont_show = (start[0], start[1] - 1, start[2])
			else: #NW
				self.dont_show = (start[0] - 1, start[1], start[2])
		else: # SW || SE
			self.dont_show = start
			if direction == 'SE':
				self.do_show = (start[0] + 1, start[1], start[2])
			else: #SW
				self.do_show = (start[0], start[1] + 1, start[2])
		self.direction = direction
		self.tile = tile
		self.on_key = str(self.do_show[0]) + '|' + str(self.do_show[1])
		self.off_key = str(self.dont_show[0]) + '|' + str(self.dont_show[1])
		
		if self.direction == 'NW':
			flipper = lambda x:(-x[0], -x[1])
			reverse = 1
		elif self.direction == 'NE':
			flipper = lambda x:(x[0], -x[1])
			reverse = 1
		elif self.direction == 'SW':
			flipper = lambda x:(x[0], -x[1])
			reverse = -1
		elif self.direction == 'SE':
			flipper = lambda x:(-x[0], -x[1])
			reverse = -1
			
		self.offsets = safe_map(flipper, _render_exceptions_coords[::reverse])
	
	def update(self):
		self.counter += 1
		if self.counter > 6:
			self.expired = True
	
	def get_offset(self):
		return self.offsets[min(6, self.counter)]
		