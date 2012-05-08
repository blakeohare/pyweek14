"""

on_circuits:
	pick 1 circuit PER CIRCUIT GROUP to indicate that that group should
	always remain on.
	A power input or output pad counts as a circuit so something like...
		---wire---[pad]---wire---
	...is 1 group, not 2.
	
	Format is a list of tuples that are (x, y, and z) coordinates. 
	You can get these from the map editor title bar

"""

_level_specific_hacks = {
	'9-0': {
		'on_circuits': [
			(1, 2, 0)
		]
	}
}

def get_hacks_for_level(name, category):
	global _level_specific_hacks
	dict = _level_specific_hacks.get(name)
	if dict != None:
		return dict.get(category)
	return None