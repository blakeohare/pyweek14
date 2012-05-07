class TileStore:
	def __init__(self):
		tiles = {}
		manifest_dir = canonicalize_path('data/tile_manifests')
		manifests = os.listdir(manifest_dir)
		for manifest in manifests:
			if '.svn' in manifest: continue
			manifest_data = read_file(manifest_dir + os.sep + manifest).split('\n')
			for line in manifest_data:
				if line != '' and line[0] != '#':
					cols = line.split('\t')
					if len(cols) >= 4:
						id = cols[0]
						images = cols[1]
						height = int(cols[2])
						flags = cols[3]
						tiles[id] = Tile(id, images, height, flags)
		self.tiles = tiles
	
	def get_tile(self, id):
		return self.tiles[id]
					
	def get_all_block_tiles(self):
		output = []
		for k in self.tiles.keys():
			if self.tiles[k].pushable:
				output.append(k)
		return output


_tile_store = None
def get_tile_store():
	global _tile_store
	if _tile_store == None:
		_tile_store = TileStore()
	return _tile_store