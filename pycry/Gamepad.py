import pygame

_cached = []

class GamepadManager:
	
	@staticmethod
	def clearAllIds():
		pass
	
	@staticmethod
	def getDeviceById(id):
		pass
	
	@staticmethod
	def getDeviceByIndex(index):
		while len(_cached) < pygame.joystick.get_count():
			_cached.append(None)
		
		js = _cached[index]
		if js == None:
			js = pygame.joystick.Joystick(js)
			js.init()
			_cached[index] = GamepadDevice(js)
		
		return js
	
	@staticmethod
	def getDeviceCount():
		return pygame.joystick.get_count()
	
	@staticmethod
	def isGamepadSupported():
		return True
	
	@staticmethod
	def platformRequiresRefresh():
		return False
	
	@staticmethod
	def refreshDevices():
		# not required by PyGame
		pass
	
	@staticmethod
	def restoreSettingsFromUserData(deviceIdOrIdList):
		pass
	
	@staticmethod
	def saveSettingsToUserData():
		pass

class GamepadDevice:
	def __init__(self, nativeJoystick):
		self.nativeJoystick = nativeJoystick
		self.axis_count = nativeJoystick.get_num_axes()
		self.hat_count = nativeJoystick.get_hat_count()
		self.button_count = nativeJoystick.get_button_count()
		self.configStack = [{}]
		self.flattened_config = {}
		self.id = None
	
	def bindAnalogAxis(self, buttonId, isPositive):
		pass
		
	def bindAnalogAxis2dX(self, buttonId, isPositive):
		pass
		
	def bindAnalogAxis2dY(self, buttonId, isPositive):
		pass
		
	def bindAnalogButton(self, buttonId):
		pass
		
	def bindDigitalAxis(self, buttonId, isPositive):
		pass
		
	def bindDigitalAxis2dX(self, buttonId, isPositive):
		pass
		
	def bindDigitalAxis2dY(self, buttonId, isPositive):
		pass
		
	def bindDigitalButton(self, buttonId):
		pass
		
	def clearBinding(self, buttonId):
		pass
		
	def clearBindings(self):
		pass
		
	def clearId(self):
		pass
		
	def flattenConfigs(self):
		pass
		
	def getAxisCount(self):
		return self.axis_count + self.hat_count * 2
		
	def getAxisState(self, index):
		if index < self.axis_count:
			return self.nativeJoystick.get_axis(index)
		index -= self.axis_count
		hat_index = index // 2
		return self.nativeJoystick.get_hat(hat_index)[index % 2] * 1.0
		
	def getButtonCount(self):
		return self.button_count
		
	def getButtonState(self, index):
		return self.nativeJoystick.get_button(index)
		
	def getCurrentState(self, buttonId):
		pass
		
	def getId(self):
		return self.id
		
	def getName(self):
		return self.nativeJoystick.get_name()
		
	def popConfig(self):
		pass
		
	def pushAutoConfigure(self):
		pass
		
	def pushEmptyConfig(self):
		pass
		
	def setId(self, id):
		self.id = id
		