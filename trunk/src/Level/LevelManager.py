_level_manager = [None, None]

def is_story_mode():
	quiet_mode = 1 == get_persistent_state().get_persisted_session_int('quiet_mode')
	return not quiet_mode

def get_level_manager():
	global _level_manager
	story_mode = is_story_mode()
	i = 1 if story_mode else 0
	if _level_manager[i] == None:
		_level_manager[i] = LevelManager(story_mode)
	return _level_manager[i]

class LevelManager:
	def __init__(self, story_mode):
		self.ordering = [
			'1-2',
			'1-3',
			'2-3',
			'3-0',
			'3-1',
			'4-0',
			'5-0',
			'6-0',
			'7-0',
			'8-0',
			'9-0',
			'10-0',
			'10-1',
			'10-2',
			'11-0',
			'12-0',
			'13-0',
			'14-0',
			'15-0',
			'16-0',
			'17-0',
			'17-1',
			'17-2',
			'17-3',
			'18-0',
			'19-0',
			'19a-0',
			'20-0',
			'24-0']
		if self.story_mode:
			self.ordering = ['intro'] + self.ordering
	
	def get_next_level(self, current_level_name):
		for i in range(self.ordering):
			if self.ordering[i] == current_level_name:
				next_i = i + 1
				if next_i < len(self.ordering):
					return next_i
				else:
					break
		return None
	
	def get_starting_level(self):
		return self.ordering[0]
	