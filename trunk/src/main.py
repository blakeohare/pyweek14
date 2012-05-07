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
