class Sprite:
	# sprite coordinates are assuming the grid is 16x16 tiles
	# these get transposed into pixel coordinates and
	# are converted into tile coords by simply dividing by 16
	def __init__(self, x, y, z, type):
		self.x = x
		self.y = y
		self.z = z
		self.dx = 0
		self.dy = 0
		self.dz = 0
		self.standingon = None
		self.ismain = type == 'main'
	
	def get_image(self, render_counter):
		img = get_image('temp_sprite.png')
		return img
	
	def pixel_position(self, xOffset, yOffset, img):
		x = self.x - self.y
		y = (self.x + self.y) // 2
		x = x - img.get_width() // 2
		y = y - self.z - img.get_height()
		return (x + xOffset, y + yOffset)
		
	def update(self):
		if self.standingon == None:
			self.dz = -2
		
		self.x += self.dx
		self.y += self.dy
		self.z += self.dz
		self.dx = 0
		self.dy = 0
		self.dz = 0
		