import time
import pygame

class _GameObj: pass

class Event:
	def __init__(self, type):
		self.type = type

class GameWindow:
	def __init__(self, title, fps, gameWidth, gameHeight, screenWidth, screenHeight):
		self.title = title
		self.fps = fps + 0.0
		self.width = gameWidth
		self.height = gameHeight
		
		pygame.init()
		self.realScreen = pygame.display.set_mode((screenWidth, screenHeight))
		pygame.display.set_caption(title)
		self.virtualScreen = pygame.Surface((gameWidth, gameHeight))
		self.lastFrame = time.time()
		self.pressed_keys = {}
	
	def pumpEvents(self):
		output = []
		sw, sh = self.realScreen.get_size()
		gw, gh = self.virtualScreen.get_size()
		pressed = pygame.key.get_pressed()
		for event in pygame.event.get():
			cEvent = None
			if event.type == pygame.MOUSEMOTION:
				cEvent = Event(EventType.MOUSE_MOVE)
				x, y = event.pos
				cEvent.x = x * gw // sw
				cEvent.y = y * gh // sh
				cEvent.down = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				cEvent = Event(EventType.MOUSE_LEFT_DOWN if event.button == 11 else EventType.MOUSE_RIGHT_DOWN)
				x, y = event.pos
				cEvent.x = x * gw // sw
				cEvent.y = y * gh // sh
				cEvent.down = True
			elif event.type == pygame.MOUSEBUTTONUP:
				cEvent = Event(EventType.MOUSE_LEFT_UP if event.button == 1 else EventType.MOUSE_RIGHT_UP)
				x, y = event.pos
				cEvent.x = x * gw // sw
				cEvent.y = y * gh // sh
				cEvent.down = False
			elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				down = event.type == pygame.KEYDOWN
				cEvent = Event(EventType.KEY_DOWN if down else EventType.KEY_UP)
				cEvent.down = down
				cEvent.key = _key_mapper.get(event.key)
				if cEvent.key == None:
					cEvent = None
				if down and event.key == pygame.K_F4 and (pressed[pygame.K_LALT] or pressed[pygame.K_RALT]):
					cEvent = Event(EventType.QUIT)
			elif event.type == pygame.QUIT:
				cEvent = Event(EventType.QUIT)
				
			if cEvent != None:
				output.append(cEvent)
		
		return output
	
	def clockTick(self):
		pygame.transform.scale(self.virtualScreen, self.realScreen.get_size(), self.realScreen)
		pygame.display.flip()
		now = time.time()
		diff = now - self.lastFrame
		delay = 1 / self.fps - diff
		if delay <= 0:
			delay = 0.001
		time.sleep(delay)
		self.lastFrame = now
	
		
EventType = _GameObj()
EventType.QUIT = 1
EventType.KEY_DOWN = 2
EventType.KEY_UP = 3
EventType.MOUSE_MOVE = 4
EventType.MOUSE_LEFT_DOWN = 5
EventType.MOUSE_LEFT_UP = 6
EventType.MOUSE_RIGHT_DOWN = 7
EventType.MOUSE_RIGHT_UP = 8

KeyboardKey = _GameObj()
KeyboardKey.UP = 1
KeyboardKey.LEFT = 2
KeyboardKey.RIGHT = 3
KeyboardKey.DOWN = 4
KeyboardKey.SPACE = 5
KeyboardKey.ENTER = 6
KeyboardKey.ESCAPE = 7
KeyboardKey.W = 8

_key_mapper = {
	pygame.K_w: KeyboardKey.W,
	pygame.K_UP: KeyboardKey.UP,
	pygame.K_DOWN: KeyboardKey.DOWN,
	pygame.K_LEFT: KeyboardKey.LEFT,
	pygame.K_RIGHT: KeyboardKey.RIGHT,
	pygame.K_RETURN: KeyboardKey.ENTER,
	pygame.K_ESCAPE: KeyboardKey.ESCAPE,
	pygame.K_SPACE: KeyboardKey.SPACE,
}
		