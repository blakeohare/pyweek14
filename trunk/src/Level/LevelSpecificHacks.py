"""

on_circuits:
	pick 1 circuit PER CIRCUIT GROUP to indicate that that group should
	always remain on.
	A power input or output pad counts as a circuit so something like...
		---wire---[pad]---wire---
	...is 1 group, not 2.
	
	Format is a list of tuples that are (x, y, and z) coordinates. 
	You can get these from the map editor title bar

moving_platforms:
	directions map to platforms in tile parser order.
	lowest y first, then lowest x, then lowest z
	
	P is pause
"""

def make_sprite(type, col, row, layer):
	return Sprite(col * 16 + 8, row * 16 + 8, layer * 8, type)

def _hack_introduce_sprites_intro(level, counter):
	
	if counter == 120:
		s = make_sprite('supervisor', 14, 0, 1)
		s.set_automation(Automation(level, 'intro_supervisor'))
		return [s]
	elif counter == 150:
		s = make_sprite('janitor', 14, 0, 1)
		s.set_automation(Automation(level, 'intro_janitor'))
		return [s]
	return []

def _hack_do_stuff_intro(playscene, level, counter):
	if counter == -1:
		playscene.player.set_automation(Automation(level, 'intro_protagonist'))


_level_specific_hacks = {
	'intro': {
		'introduce_sprites': _hack_introduce_sprites_intro,
		'do_stuff': _hack_do_stuff_intro
	},
	
	'9-0': {
		'on_circuits': [
			(1, 2, 0)
		]
	},
	
	'15-0': {
		'moving_platforms': [
			'NW P P SE SE SE P P NW NW', 
			'SW P P NE NE NE P P SW SW'
		]
	}
}

def get_hacks_for_level(name, category):
	global _level_specific_hacks
	dict = _level_specific_hacks.get(name)
	if dict != None:
		return dict.get(category)
	return None