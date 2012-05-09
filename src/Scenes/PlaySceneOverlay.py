class PlaySceneOverlay:
	def __init__(self, playscene, level):
		self.playscene = playscene
		self.level = level
	
	def render(self, screen, render_counter):
		img = get_text("[temp UI] De-Goo: " + str(get_persisted_level_int('decontaminant')), 18, (0, 255, 0))
		screen.blit(img, (5, 5))