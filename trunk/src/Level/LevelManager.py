_level_manager = [None, None]

def is_story_mode():
	quiet_mode = 1 == get_persisted_session_int('quiet_mode')
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
				('1-3', "Lab Entrance", (4, 9, 1, 'ne')),
				('2-3', None, (7, 13, 1, 'ne')),
				('3-1', "The Green Room", (9, 10, 1, 'ne')),
				('4-0', None, (5, 8, 1, 'ne')),
				('5-0', None, (2, 10, 1, 'ne')),
				('6-0', None, (1, 9, 3, 'ne')),
				('7-0', None, (1, 11, 3, 'ne')),
				('8-0', None, (6, 9, 1, 'ne')),
				('9-0', None, (1, 7, 1, 'ne')),
				('10-2', None, (5, 11, 1, 'ne')),
				('11-0', None, (1, 4, 3, 'se')),
				('12-0', None, (1, 10, 3, 'ne')),
				('13-0', None, (7, 18, 1, 'ne')),
				('14-0', None, (5, 10, 3, 'ne')),
				('15-0', None, (1, 10, 2, 'ne')),
				('16-0', None, (10, 16, 2, 'ne')),
				('17-3', None, (9, 18, 3, 'ne')),
				('18-0', None, (1, 19, 2, 'se')),
				('19a-0', None, (2, 7, 1, 'se')),
				('19b-1', None, (1, 17, 1, 'se')),
				('19-0', None, (1, 8, 1, 'se')),
				('20-0', None, (1, 15, 2, 'se')),
				('21-0', None, (9, 13, 2, 'ne')),
				('flipmaze', None, (1, 19, 1, 'se')),
				('25-0', None, (1, 12, 1, 'se')),
				('24-0', None, (1, 20, 3, 'ne')),
				('26-0', None, (1, 9, 1, 'se')),
				('27-0', None, (1, 9, 1, 'se')),
				('90-0', None, (1, 9, 3, 'se'))]
		if story_mode:
			self.ordering = [('intro', "Your Office", (12, 14, 1, 'nw'))] + self.ordering
	
	def get_current_level_index(self, current_level_name):
		for i in range(len(self.ordering)):
			if self.ordering[i][0] == current_level_name:
				return i
		return None
	
	def get_current_room_name(self, current_level_name):
		return self.ordering[self.get_current_level_index(current_level_name)][1]
	
	def get_next_level(self, current_level_name):
		i = self.get_current_level_index(current_level_name)
		next_i = i + 1
		if next_i < len(self.ordering):
			return self.ordering[next_i][0]
		return None
	
	def get_starting_point_for_level(self, name):
		i = self.get_current_level_index(name)
		if len(self.ordering[i]) >= 3:
			return self.ordering[i][2]
		return None
	
	def get_starting_level(self):
		return self.ordering[0]
	