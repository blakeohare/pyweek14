_debug_message = None
def set_user_debug_message(text):
	global _debug_message
	_debug_message = text

def get_user_debug_message():
	global _debug_message
	return _debug_message			

def main():

	pygame.init()
	real_screen = pygame.display.set_mode((800, 600))
	fake_screen = pygame.Surface((400, 300))
	fps = 60

	pressed = {
		'start': False,
		'left': False,
		'right': False,
		'down': False,
		'up': False,
		'action': False
	}
	
	load_persistent_state()
	
	if os.path.exists('start.txt'):
		lines = trim(read_file('start.txt').split('\n'))
		
		if lines[0] == 'normal':
			active_scene = MainMenuScene()
		else:
			level_name = lines[0]
			active_scene = PlayScene(level_name)
			if not active_scene.do_not_override_start:
				coords = safe_map(int, lines[1].split(','))
				x = coords[0]
				y = coords[1]
				z = 8
				active_scene.player.x = x * 16 + 8
				active_scene.player.y = y * 16 + 8
				active_scene.player.z = z * 8
			
	else:
		active_scene = MainMenuScene()
	counter = 0
	
	input_manager = get_input_manager()
	
	while active_scene != None:
		start = time.time()
		
		counter += 1
		event_list = []
		event_list = input_manager.get_events()
		pressed = input_manager.my_pressed
		try_quit = input_manager.quitAttempt
		axes = input_manager.axes
		mouse_events = input_manager.get_mouse_events()
		
		active_scene.process_input(event_list, pressed, axes, mouse_events)
		active_scene.update(counter)
		
		fake_screen.fill((0, 0, 0))
		active_scene.render(fake_screen, counter)
		
		debug_message = get_user_debug_message()
		if debug_message != None:
			fake_screen.blit(get_text(debug_message, 20, (255, 0, 0)), (10, 10))
		
		pygame.transform.scale(fake_screen, (real_screen.get_width(), real_screen.get_height()), real_screen)
		
		active_scene = active_scene.next
		
		if try_quit:
			active_scene = None
			
		pygame.display.flip()
		
		end = time.time()
		
		diff = end - start
		if diff == 0:
			rate = 'inf'
		else:
			rate = 1.0 / diff
		delay = 1.0 / fps - diff
		if delay > 0:
			time.sleep(delay)
		else:
			pass #print "----FRAME RATE DIPPING!!!!-----"
		#print rate
