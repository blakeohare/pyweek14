_sound_store = {}
_sound_initialized = False
def play_sound(path):
	global _sound_store, _sound_initialized
	if _sound_initialized == False:
		pygame.mixer.init()
	snd = _sound_store.get(path)
	if snd == None:
		fpath = 'sound/SFX/' + path
		fpath = fpath.replace('/', os.sep).replace('\\', os.sep)
		snd = pygame.mixer.Sound(fpath)
		_sound_store[path] = snd
	snd.play()
