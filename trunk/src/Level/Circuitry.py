def make_key(x, y, z):
	return str(str(x) + '|' + str(y) + '|' + str(z))

def make_ckey(c):
	return str(c[0]) + '|' + str(c[1]) + '|' + str(c[2])

class Circuits:
	def __init__(self, level):
		self.level = level
		self.refresh_groups()
		
	def refresh_charges(self):
		on_circuits = get_hacks_for_level(self.level.name, 'on_circuits')
		active_input_panels = []
		for input_panel in self.power_in:
			x = input_panel[0]
			y = input_panel[1]
			z = input_panel[2]
			lookup = self.level.cellLookup[x][y]
			if z + 1 < len(lookup):
				ti = lookup[z + 1]
				if ti != None:
					t = self.level.grid[x][y][ti]
					if t != None and t.id == '45':
						active_input_panels.append(input_panel)
		on_groups = safe_map(lambda x: self.groups_by_coords[make_ckey(x)], on_circuits + active_input_panels)
		group_id = 1
		max_group_id = len(self.coords_by_group) - 1
		while group_id <= max_group_id:
			is_group_on = group_id in on_groups
			for coord in self.coords_by_group[group_id]:
				tile = self.level.get_tile_at(coord)
				if tile.actual_circuit:
					id = tile.id
					if id.endswith('on'):
						id = id[:-2]
					id = ((id + 'on') if is_group_on else id)
					tile = get_tile_store().get_tile(id)
					self.level.modify_block(coord[0], coord[1], coord[2], tile)
					#print "Turning " + str(coord) + ' '+ ("on" if is_group_on else "off")
			group_id += 1
		self.on_groups = on_groups
		
	def refresh_groups(self):
		self.groups = []
		
		grid = self.level.grid
		width = self.level.width
		height = self.level.height
		circuits = []
		circuits_by_loc = {}
		self.power_in = []
		y = 0
		while y < height:
			x = 0
			while x < width:
				stack = grid[x][y]
				z = 0
				for item in stack:
					if item == None:
						z += 1
					else:
						if item.circuit:
							circuits.append((x, y, z))
							circuits_by_loc[str(x)+'|' + str(y) + '|' + str(z)] = []
						if item.power_input:
							self.power_in.append((x, y, z))
						z += item.height
				x += 1
			y += 1
		
		tags = {} # key -> group name
		
		for circuit in circuits:
			x = circuit[0]
			y = circuit[1]
			z = circuit[2]
			neighbors = [
				circuits_by_loc.get(make_key(x, y - 1, z)),
				circuits_by_loc.get(make_key(x, y + 1, z)),
				circuits_by_loc.get(make_key(x + 1, y, z)),
				circuits_by_loc.get(make_key(x - 1, y, z))]
			for neighbor in neighbors:
				if neighbor != None:
					neighbor.append(circuit)
		
		group_id = 0
		while len(circuits) > 0:
			group_id += 1
			circuit = circuits.pop()
			while tags.get(make_ckey(circuit)) != None:
				if len(circuits) > 0:
					circuit = circuits.pop()
				else:
					circuit = None
					break
			if circuit != None:
				queue = [circuit]
				while len(queue) > 0:
					item = queue.pop()
					k = make_ckey(item)
					tags[k] = group_id
					for neighbor in circuits_by_loc[k]:
						if tags.get(make_ckey(neighbor)) == None:
							tags[make_ckey(neighbor)] = group_id
							queue.append(neighbor)
		
		groups_to_coords = [[]]
		for k in tags.keys():
			group_id = tags[k]
			while len(groups_to_coords) <= group_id:
				groups_to_coords.append([])
			coords = safe_map(int, k.split('|'))
			groups_to_coords[group_id].append((coords[0], coords[1], coords[2]))
		self.coords_by_group = groups_to_coords
		self.groups_by_coords = tags
		
		self.refresh_charges()
	
	def is_charged(self, x, y, z):
		k = make_key(x, y, z)
		group_id = self.groups_by_coords.get(k, 0)
		if group_id > 0:
			return group_id in self.on_groups
		return False
		