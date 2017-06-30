class CoilManager:
	
	def __init__(self, level):
		pass
	
	def set_fresh_coils(self, coils):
		self.coils = coils
	
	def find_zapped_sprites(self, sprites):
		coil_map = []
		for coil in self.coils:
			x = coil[0]
			while len(coil_map) <= x:
				coil_map.append([])
			coil_map[x].append(coil)
		
		for sprite in sprites:
			if sprite.death_counter < 0 and (sprite.main_or_hologram or sprite.israt):
				col = int(sprite.x // 16)
				while col + 2 >= len(coil_map):
					coil_map.append([])
				
				i = col - 1
				while i <= col + 1:
					coil_column = coil_map[i]
					for coil in coil_column:
						if Math.abs(coil[2] - int(sprite.z // 8)) < 2:
							dx = coil[0] * 16 + 8 - sprite.x
							dy = coil[1] * 16 + 8 - sprite.y
							if dx * dx + dy * dy < 24 * 24:
								sprite.death_counter = 90
								sprite.death_type = 'bazat'
								sprite.immobilized = True
								
					i += 1
			