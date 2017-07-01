import random

def randomFloat():
	return random.random()

def randomBool():
	return random.random() < .5

_INT32_MAX = 2 ** 31 - 1
def randomInt(mn = None, mx = None):
	if mn == None:
		return int(random.random() * _INT32_MAX)
	if mx == None:
		return int(random.random() * mn)
	return mn + int(random.random() * (mx - mn))
