import pygame
import time
import math
import os
import random


_fonts = {}
def get_font(size):
	global _fonts
	key = 'f' + str(size)
	font = _fonts.get(key)
	if font == None:
		font = pygame.font.SysFont(pygame.font.get_default_font(), size)
		_fonts[key] = font
	return font

_text = {}
def get_text(text, size, color):
	global _text
	key = str(size) + "," + str(color) + "|" + text
	image = _text.get(key)
	if image == None:
		font = get_font(size)
		image = font.render(text, True, color)
		_text[key] = image
	return image

_image_library = {}

def get_image(path):
	global _image_library
	image = _image_library.get(path)
	if image == None:
		image = pygame.image.load(canonicalize_path('images/' + path))
		_image_library[path] = image
	return image


class Level:
	
	def __init__(self, name):
		self.name = name
		self.initialize()
	
	def initialize(self):
		lines = read_file('data/levels/' + self.name + '.txt').split('\n')
		values = {}
		for line in lines:
			line = trim(line)
			if len(line) > 0 and line[0] == '#':
				parts = line.split(':')
				if len(parts) > 1:
					key = parts[0][1:]
					value = ':'.join(parts[1:])
					values[key] = value
		self.values = values
		
		self.width = int(self.values['width'])
		self.height = int(self.values['height'])
		self.initialize_tiles(self.values['tiles'].split(','))
	
	def initialize_tiles(self, tiles):
		width = self.width
		height = self.height
		grid = make_grid(self.width, self.height, None)
		references = make_grid(self.width, self.height, None)
		
		tilestore = get_tile_store()
		i = 0
		for tile in tiles:
			x = i % width
			y = i // width
			tileStack = []
			referenceStack = []
			grid[x][y] = tileStack
			references[x][y] = referenceStack
			cells = tile.split('|')
			
			if len(cells) == 1 and len(cells[0]) == 0:
				pass
			else:
				for cell in cells:
					
					if cell == '0':
						referenceStack.append(len(tileStack))
						tileStack.append(None)
					else:
						t = tilestore.get_tile(cell)
						z = 0
						while z < t.height:
							referenceStack.append(len(tileStack) - 1)
							z += 1
						
						tileStack.append(t)
				
			
			i += 1
		self.grid = grid
		self.cellLookup = references
	
	def render(self, screen, xOffset, yOffset, sprites, render_counter):
		width = self.width
		height = self.height
		sprite_lookup = {}
		for sprite in sprites:
			x = sprite.x // 16
			y = sprite.y // 16
			key = str(x) + '_' + str(y)
			list = sprite_lookup.get(key)
			if list == None:
				list = []
				sprite_lookup[key] = list
			list.append(sprite)
		#print sprite_lookup
		empty_list = []
		
		i = 0
		while i < width + height:
			col = i
			row = 0
			
			while row < height and col >= 0:
				if col < width:
					sprite_list = sprite_lookup.get(str(col) + '_' + str(row))
					
					self.render_tile_stack(screen, col, row, xOffset, yOffset, render_counter, sprite_list)
				row += 1
				col -= 1
			i += 1
	
	def render_tile_stack(self, screen, col, row, xOffset, yOffset, render_counter, sprites):
		stack = self.grid[col][row]
		cumulative_height = 0
		x = xOffset + col * 16 - row * 16
		y = yOffset + col * 8 + row * 8
		for tile in stack:
			if sprites != None:
				new_sprites = []
				for sprite in sprites:
					if sprite.z < cumulative_height:
						img = sprite.get_image(render_counter)
						coords = sprite.pixel_position(xOffset, yOffset, img)
						screen.blit(img, coords)
					else:
						new_sprites.append(sprite)
				sprites = new_sprites
			if tile == None:
				cumulative_height += 8
			else:
				tile.render(screen, x, y - cumulative_height, render_counter)
				cumulative_height += tile.height * 8
		if sprites != None and len(sprites) > 0:
			sprites = sorted(sprites, lambda x:x.z)
			for sprite in sprites:
				img = sprite.get_image(render_counter)
				coords = sprite.pixel_position(xOffset, yOffset, img)
				screen.blit(img, coords)

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
		self.pushable = 'b' in flags
		self.blocking = 'x' in flags
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
		

class TileStore:
	def __init__(self):
		tiles = {}
		manifest_dir = canonicalize_path('data/tile_manifests')
		manifests = os.listdir(manifest_dir)
		for manifest in manifests:
			if '.svn' in manifest: continue
			manifest_data = read_file(manifest_dir + os.sep + manifest).split('\n')
			for line in manifest_data:
				if line != '' and line[0] != '#':
					cols = line.split('\t')
					if len(cols) >= 4:
						id = cols[0]
						images = cols[1]
						height = int(cols[2])
						flags = cols[3]
						tiles[id] = Tile(id, images, height, flags)
		self.tiles = tiles
	
	def get_tile(self, id):
		return self.tiles[id]
					
			


_tile_store = None
def get_tile_store():
	global _tile_store
	if _tile_store == None:
		_tile_store = TileStore()
	return _tile_store

class PlayScene:
	def __init__(self, level_name):
		self.next = self
		self.level_name = level_name
		self.level = Level(level_name)
		self.player = Sprite(17, 17, 32, 'main')
		self.sprites = [self.player]
		
	def process_input(self, events, pressed):
		pass
	
	def update(self, counter):
		for sprite in self.sprites:
			sprite.update()
	
	def render(self, screen, counter):
		self.level.render(screen, screen.get_width() / 2, 50, self.sprites, counter)
		

class TitleScene:
	def __init__(self):
		self.next = self
		self.text = get_text(
			"If you can read this, then you are",
			24, (255, 255, 0))
		self.textb = get_text(
			"100% set up to use Python + PyGame",
			24, (255, 255, 0))
		self.x = 0
		self.y = 0

	def process_input(self, events, pressed):
		pass
	
	def update(self, counter):
		self.x += 1
		self.y += 2
	
	def render(self, screen, counter):
		w = screen.get_width()
		h = screen.get_height()
		self.x = (self.x + w) % w
		self.y = (self.y + h) % h
		
		for t in ((0, 0), (-1, 0), (0, -1), (-1, -1)):
			x = self.x + w * t[0]
			y = self.y + h * t[1]
			screen.blit(self.text, (x, y))
			screen.blit(self.textb, (x, y + self.textb.get_height() + 4))
			

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
		

def trim(string):
	while len(string) > 0 and string[0] in ' \n\r\t':
		string = string[1:]
	while len(string) > 0 and string[-1] in ' \r\n\t':
		string = string[:-1]
	return string

def canonicalize_path(path):
	return path.replace('\\', os.sep).replace('/', os.sep)

def read_file(path):

	c = open(canonicalize_path(path), 'rt')
	t = c.read()
	c.close()
	return t
	
def write_file(path, contents):
	c = open(canonicalize_path(path), 'wt')
	c.write(contents)
	c.close()

def make_grid(width, height, defaultValue):
	cols = []
	x = 0
	while x < width:
		col = []
		y = 0
		while y < height:
			col.append(defaultValue)
			y += 1
		cols.append(col)
		x += 1
	return cols

def safe_map(function, list):
	i = 0
	l = len(list)
	output = []
	while i < l:
		output.append(function(list[i]))
		i += 1
	return output


def go_fast(): return True

class MyEvent:
	def __init__(self, key, down):
		self.key = key
		self.down = down
		self.up = not down

_key_mapping = {
	pygame.K_RETURN: 'start',
	pygame.K_LEFT: 'left',
	pygame.K_RIGHT: 'right',
	pygame.K_UP: 'up',
	pygame.K_DOWN: 'down',
	pygame.K_SPACE: 'action'
}
def get_inputs(event_list, pressed, isometric):
	global _key_mapping
	pg_pressed = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type in (pygame.KEYDOWN, pygame.KEYUP):
			down = event.type == pygame.KEYDOWN
			if down and event.key == pygame.K_F4:
				if pg_pressed[pygame.K_LALT] or pg_pressed[pygame.K_RALT]:
					return True
			elif down and event.key == pygame.K_ESCAPE:
				return True
			
			my_key = _key_mapping.get(event.key)
			if my_key != None:
				my_event = MyEvent(my_key, down)
				event_list.append(my_event)
				pressed[my_key] = down
		elif event.type == pygame.QUIT:
			return True
	
	x_axis = 0
	y_axis = 0
	
	if pressed['left']:
		x_axis = -2
	elif pressed['right']:
		x_axis = 2
	if pressed['up']:
		y_axis = -2
	elif pressed['down']:
		y_axis = 2
	
	fx_axis = x_axis
	fy_axis = y_axis
	if isometric:
		fx_axis = x_axis + y_axis
		fy_axis = -x_axis + y_axis
		x_axis = fx_axis
		y_axis = fy_axis
	
	pressed['x-axis'] = x_axis
	pressed['y-axis'] = y_axis
	
	return False
			

def main():

	pygame.init()
	real_screen = pygame.display.set_mode((800, 600))
	fake_screen = pygame.Surface((400, 300))
	fps = 60 if go_fast() else 30
	
	pressed = {
		'start': False,
		'left': False,
		'right': False,
		'down': False,
		'up': False,
		'action': False,
		'x-axis': 0,
		'y-axis': 0
	}
	
	playscene_type = str(PlayScene('1-2'))
	
	active_scene = PlayScene('1-2')
	counter = 0
	while active_scene != None:
		
		start = time.time()
		
		counter += 1
		
		event_list = []
		try_quit = get_inputs(event_list, pressed, str(active_scene) == playscene_type)
		
		active_scene.process_input(event_list, pressed)
		active_scene.update(counter)
		
		fake_screen.fill((0, 0, 0))
		active_scene.render(fake_screen, counter)
		
		pygame.transform.scale(fake_screen, (real_screen.get_width(), real_screen.get_height()), real_screen)
		
		active_scene = active_scene.next
		
		if try_quit:
			active_scene = None
			
		pygame.display.flip()
		
		end = time.time()
		
		diff = end - start
		delay = 1.0 / fps - diff
		if delay > 0:
			time.sleep(delay)
		# TODO: print FPS when in debug mode


main()