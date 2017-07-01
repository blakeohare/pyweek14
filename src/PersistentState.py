# persistent state cannot save strings with newlines across "forever" sessions

_persistent_state = None

def get_persistent_state():
	global _persistent_state
	if _persistent_state == None:
		_persistent_state = PersistentState()
	return _persistent_state

def load_persistent_state():
	get_persistent_state().load_game()

def save_persistent_state():
	get_persistent_state().save_game()

def get_persisted_forever_int(name):
	return get_persistent_state().get_int_forever(name)
def get_persisted_session_int(name):
	return get_persistent_state().get_int_session(name)
def get_persisted_level_int(name):
	return get_persistent_state().get_int_level(name)

def get_persisted_forever_string(name):
	return get_persistent_state().get_string_forever(name)
def get_persisted_session_string(name):
	return get_persistent_state().get_string_session(name)
def get_persisted_level_string(name):
	return get_persistent_state().get_string_level(name)

def set_persisted_forever_int(name, value):
	return get_persistent_state().set_int_forever(name, value)
def set_persisted_session_int(name, value):
	return get_persistent_state().set_int_session(name, value)
def set_persisted_level_int(name, value):
	return get_persistent_state().set_int_level(name, value)

def set_persisted_forever_string(name, value):
	return get_persistent_state().set_string_forever(name, value)
def set_persisted_session_string(name, value):
	return get_persistent_state().set_string_session(name, value)
def set_persisted_level_string(name, value):
	return get_persistent_state().set_string_level(name, value)

def increment_persisted_forever_int(name, amount):
	set_persisted_forever_int(name, get_persisted_forever_int(name) + amount)

def increment_persisted_level_int(name, amount):
	set_persisted_level_int(name, get_persisted_level_int(name) + amount)

def increment_persisted_session_int(name, amount):
	set_persisted_session_int(name, get_persisted_session_int(name) + amount)

def persistence_change_level():
	get_persistent_state().level = {}

class PersistentState:
	def __init__(self):
		self.forever = {}
		self.session = {}
		self.level = {}
	
	def purge_all(self):
		self.forever = {}
		self.session = {}
		self.level = {}
	
	def save_game(self):
		UserData.fileWriteText('save.txt', self.serialize())
	
	def change_level(self):
		self.level = {}
	
	def serialize(self):
		output = []
		for key in self.forever.keys():
			value = self.forever[key]
			if value[1] == None:
				value[1] = ''
			output.append(value[0] + key + ':' + str(value[1]))
		return '\n'.join(output)
	
	def load_game(self):
		t = None
		if UserData.fileExists('save.txt'):
			t = UserData.fileReadText('save.txt')
		values = {}
		if t != None:
			lines = t.split('\n')
			for line in lines:
				parts = line.split(':')
				if len(parts) >= 2:
					key = parts[0]
					value = ':'.join(parts[1:])
					if len(key) >= 2:
						type = key[0]
						name = key[1:]
						if type == 'i':
							try:
								value = Core.parseInt(value)
							except:
								value = 0
							
						else:
							type = 's'
						values[name] = (type, value)
		self.forever = values
	
	def set_int_forever(self, name, value):
		self._set_int(name, value, self.forever)
	
	def set_int_session(self, name, value):
		self._set_int(name, value, self.session)
	
	def set_int_level(self, name, value):
		self._set_int(name, value, self.level)
	
	def get_int_forever(self, name):
		return self._get_int(name, self.forever)
	
	def get_int_session(self, name):
		return self._get_int(name, self.session)
	
	def get_int_level(self, name):
		return self._get_int(name, self.level)
	
	def set_string_forever(self, name, value):
		self._set_string(name, value, self.forever)
	
	def set_string_session(self, name, value):
		self._set_string(name, value, self.session)
	
	def set_string_level(self, name, value):
		self._set_string(name, value, self.level)
	
	def get_string_forever(self, name):
		return self._get_string(name, self.forever)
	
	def get_string_session(self, name):
		return self._get_string(name, self.session)
	
	def get_string_level(self, name):
		return self._get_string(name, self.level)
	
	def _set_int(self, name, value, lookup):
		lookup[name] = ('i', value)
	
	def _set_string(self, name, value, lookup):
		lookup[name] = ('s', value)
	
	def _get_int(self, name, lookup):
		value = lookup.get(name)
		if value != None and value[0] == 'i':
			return value[1]
		return 0
	
	def _get_string(self, name, lookup):
		value = lookup.get(name)
		if value != None and value[0] == 's':
			return value[1]
		return ''