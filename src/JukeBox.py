_MUSIC_ENABLED = True

_jukebox = None

def get_jukebox():
	global _jukebox
	if _jukebox == None:
		_jukebox = JukeBox()
	return _jukebox

def play_sound(path):
	if is_music_off(): return
	get_jukebox().play_sound(path)

def is_music_off():
	return not _MUSIC_ENABLED

class JukeBox:
	def __init__(self):
		pygame.mixer.init()
		self.current = None
		
		ps = get_persistent_state()
		if (ps.forever.get('sfx') != None):
			self.set_music_volume(ps.get_int_forever('music'))
			self.set_sfx_volume(ps.get_int_forever('sfx'))
		else:
			self.set_music_volume(70)
			self.set_sfx_volume(70)
		self.sounds = {}
		self.music_map = {
			'intro':'biologytake2',
			'12-0':'chemistry',
			'13-0':'chemistry',
			'14-0':'chemistry',
			'17-3':'chemistry',
			'18-0':'chemistry',
			'19a-0':'chemistry',
			'19b-1':'chemistry',
			'19-0':'chemistry',
			'99-0':'bossmusic',
		}
		
		
	def get_song_normalization(self, name):
		if name == 'title':
			return 1
		
		return .3
	
	def set_music_volume(self, percent):
		percent = max(0, min(100, Math.floor(percent)))
		self.music_volume = percent
		self.update_volume(self.current)
	
	def update_volume(self, song):
		if song != None:
			volume = self.music_volume * self.get_song_normalization(song)
			pygame.mixer.music.set_volume(volume / 100.0)
	
	def set_sfx_volume(self, percent):
		percent = max(0, min(100, Math.floor(percent)))
		self.sfx_volume = percent
		self.sounds = {}
	
	def get_music_volume(self):
		return self.music_volume
	
	def get_sfx_volume(self):
		return self.sfx_volume
	
	def play_sound(self, path):
		if '.' in path:
			raise Exception("Do not include file extension in play_sound")

		if is_music_off(): return

		snd = self.sounds.get(path)
		if snd == None:
			fpath = ('sound/sfx/' + path + '.ogg').replace('/', os.sep)
			snd = self.sounds.get(fpath)
			if snd == None:
				snd = pygame.mixer.Sound(fpath)
				volume = self.sfx_volume / 100.0
				if path.startswith('talk'):
					if 'high' in path:
						volume = volume / 2
					volume = volume / 3
				if 'menumove' in path:
					volume = volume / 4
				snd.set_volume(volume)
				self.sounds[path] = snd
			else:
				self.sounds[path] = snd
		snd.play()
	
	def ensure_current_song(self, song):
		if is_music_off(): return
		if song == 'bossmusic' and self.current == 'stringtheory':
			self.ensure_current_song('stringtheory')
			return

		if song == None:
			pygame.mixer.music.stop()
			return
		
		song = 'sound/music/' + song + '.ogg'
		song = song.replace('/', os.sep)
		if self.current != song:
			self.current = song
			self.update_volume(song)
			pygame.mixer.music.load(song)
			pygame.mixer.music.play(-1)

	def get_song_for_level(self, level):
		return self.music_map.get(level, 'astrophysics')
	
	def update(self, levelname):
		song = self.get_song_for_level(levelname)
		#if levelname == '99-0' and self.current == 'stringtheory' and song != 'stringtheory':
			
		#	#return
			
		self.ensure_current_song(song)
