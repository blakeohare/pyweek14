def flags_contains(flags, items):
	for c in items:
		if c in flags:
			return True
	return False

class Tile:
	def is_num(self, string):
		return string in '0123456789'
		
	def __init__(self, id, images, height, flags):
		self.id = id
		images = images.split('|')
		self.framerate = 4
		if self.is_num(images[0][0]):
			self.framerate = int(images[0])
			images = images[1:]
		self.images = safe_map(lambda x:get_image('tiles/' + x), images)
		self.still = len(self.images) == 1
		self.still_image = self.images[0]
		self.y_offsets = safe_map(lambda x:24 - x.get_height(), self.images)
		self.still_y_offset = self.y_offsets[0]
		self.image_count = len(self.images)
		self.height = height
		self.pushable = flags_contains(flags, 's')
		self.blocking = flags_contains(flags, 'x')
		self.stairs = flags_contains(flags, '12345678')
		self.blocking = self.blocking or self.stairs or self.pushable
		if self.stairs:
			double = flags_contains(flags, '5678')
			topo = 2 if double else 1
			if flags_contains(flags, '15'):
				self.topography = [0, -topo, -topo, 0]
				self.entrance = 'SE'
			elif flags_contains(flags, '26'):
				self.topography = [0, 0, -topo, -topo]
				self.entrance = 'SW'
			elif flags_contains(flags, '37'):
				self.topography = [-topo, 0, 0, -topo]
				self.entrance = 'NW'
			elif flags_contains(flags, '48'):
				self.topography = [-topo, -topo, 0, 0]
				self.entrance = 'NE'
				
		# TODO: go through manifest and add them all
	
	def render(self, screen, x, y, render_counter):
		
		if self.still:
			img = self.still_image
			y += self.still_y_offset
		else:
			i = (render_counter // self.framerate) % self.image_count
			img = self.images[i]
			y += self.y_offsets[i]
		
		screen.blit(img, (x, y))
		