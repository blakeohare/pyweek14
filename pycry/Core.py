import time

def parseInt(value):
	try:
		return int(value)
	except:
		raise Exception("Not an integer: '" + value + "'")

def sleep(seconds):
	time.sleep(seconds * 1.0)
