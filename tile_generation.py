import copy, pickle
from string import ascii_uppercase
points = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10}
for ind, val in enumerate()
letters = copy.deepcopy(points)
distribution = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]

bag = dict()

# def tile_maker_fn(self):


class Tile(object):
	def __init__(self, letter):
		self.letter = letter
		self.points = points[self.letter]

	def make_tile(self, game = None):
		new = copy.deepcopy(self)
		if game:
			new.game = game
		return new

	def __repr__(self):
		return self.letter


for ind, letter in enumerate(ascii_uppercase):


