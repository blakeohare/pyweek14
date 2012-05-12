class PlaySceneOverlay:
	def __init__(self, playscene, level):
		self.playscene = playscene
		self.level = level
	
	def pad_with_zeroes(self, num, digits):
		s = str(num)
		while len(s) < digits:
			s = '0' + s
		return s
	
	def render(self, screen, render_counter):
		bg = get_image('misc/status_overlay.png')
		goo = get_image('tiles/mediumdegoo.png')
		rp = get_image('tiles/researchpapers.png')

		screen.blit(bg, (0, screen.get_height() - bg.get_height()))
		screen.blit(goo, (0, screen.get_height() - goo.get_height() - 14))
		screen.blit(rp, (24, screen.get_height() - rp.get_height() - 0))
		
		research_saved = get_persisted_forever_int('research')
		session_research = get_persisted_session_int('research')
		level_research = get_persisted_level_int('research')
		r = research_saved + level_research + session_research
		
		goo_count = get_text(self.pad_with_zeroes(get_persisted_level_int('decontaminant'), 3), 16, (100, 255, 100))
		rp_count = get_text(self.pad_with_zeroes(r, 3), 16, (255, 255, 255))
		loc = get_level_manager().get_current_room_name(self.level.name)
		if loc == None:
			loc = "Room Needs Name"
		loc = get_text(loc, 12, (255, 255, 255))
		
		screen.blit(goo_count, (30, screen.get_height() - goo.get_height() - 5))
		screen.blit(rp_count, (54, screen.get_height() - rp.get_height() + 11))
		screen.blit(loc, (screen.get_width() - 90, screen.get_height() - loc.get_height() - 4))
		