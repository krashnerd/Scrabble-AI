
class Tile(object):
	def __init__(self, letter, points = None, tile_id = None):
		self.letter = letter
		self.tile_id = tile_id
		self.points = points if points is not None else consts.points[letter]

	def __hash__(self):
		return hash((self.letter, self.tile_id))

	def __repr__(self):
		return self.letter
