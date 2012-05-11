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
		self.hascharge = False
		self.images = safe_map(lambda x:get_image('tiles/' + x), images)
		self.still = len(self.images) == 1
		self.still_image = self.images[0]
		self.y_offsets = safe_map(lambda x:24 - x.get_height(), self.images)
		self.still_y_offset = self.y_offsets[0]
		self.image_count = len(self.images)
		self.height = height
		self.no_blocks = False
		self.pushable = flags_contains(flags, 's')
		self.blocking = flags_contains(flags, 'x')
		self.circuit = flags_contains(flags, 'eh')
		self.actual_circuit = flags_contains(flags, 'e')
		self.stairs = flags_contains(flags, '12345678')
		self.teleporter = id == 't1'
		self.power_input = id == 'pi'
		self.power_output = id == 'po'
		self.cant_push_over = flags_contains(flags, 'n')
		self.research = id == '41'
		self.goo = id in ('42', '43', '44')
		self.isswitch = id in ('pi', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7')
		self.powerup = self.research or self.goo
		self.is_goo = id == '15'
		self.goo_size = 0
		if self.goo:
			self.goo_size = ((int(id) - 41) - 1) * 2 + 1 # 1, 3, 5 OMGHAX
		self.blocking = self.blocking or self.stairs or self.pushable
		if self.stairs:
			self.no_blocks = True
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
			
	# Code duplicated below
	def get_image(self, render_counter):
		if self.still:
			return self.still_image
		i = (render_counter // self.framerate) % self.image_count
		return self.images[i]

	# Code duplicated above
	def render(self, screen, x, y, render_counter):
		
		if self.still:
			img = self.still_image
			y += self.still_y_offset
		else:
			i = (render_counter // self.framerate) % self.image_count
			img = self.images[i]
			y += self.y_offsets[i]
		
		screen.blit(img, (x, y))
		