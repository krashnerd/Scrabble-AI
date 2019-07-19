import json, string
import build_dictionary, consts

from numpy import random
from Board import Board
from collections import OrderedDict

class GameError(Exception):
	pass

class TileNotFoundError(GameError):
	def __init__(self, expression, message):
		self.expression = expression
		self.message = "Tile not found in player rack"

class Rack():
	def __init__(self, game, player):
		self.game = game
		self.player = player

		self.tiles = []

	def add_tiles(self, tiles):
		self.tiles.extend(tiles)

	def has_tiles(self, move):
		for tile, position in move:
			if tile not in self:
				return False

		return True

	def make_move(self, move):
		try:
			for tile, _ in move:
				self.tiles.remove(tile)
		
		except ValueError:
			raise TileNotFoundError

		else:
			self.add_tiles(game.bag.pull_tiles(self.tiles_needed()))


	def tiles_needed(self):
		return 7 - len(self.tiles)

	def __contains__(self, item):
		return item in self.tiles



class Player:
	def __init__(self, game):
		self.game = game
		self.rack = Rack(self.game, self)

	def make_move(self):
		pass

class HumanPlayer(Player):
	def __init__(self, game):
		Player.__init__(game)




class Scrabble(object):
	def __init__(self, num_players = 2):
		self.letter_dist = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]
		points = {1:"AEIOULNSTR",2:"DG",3:"BCMP",4:"FHVWY",5:"K",8:"JX",10:"QZ"}
		self.points = dict() # dictionary for point values of each letter
		for num, letters in points.items():
			for letter in letters:
				self.points[letter] = num

		self.points2 = OrderedDict()
		for ind, letter in enumerate(string.ascii_uppercase):
			self.points2[letter] = self.points[letter]

		output_str = json.dumps(self.points2)
		with open("points.txt", "w") as outfile:
			outfile.write(output_str)
			exit(0)

		self.bag = Bag(self)
		self.board = Board(self)
		self.dictionary = build_dictionary.get_dictionary("dictionary/dict.bytesIO")
		self.check_word = lambda word:build_dictionary.check_word(word, self.dictionary)


	def score(word):
		points = 0
		for tile in word:
			points += tile.points * 2
		if len(word) == 7:
			points += 50
		return points

	def score_word(self, locs):
		return self.board.score_word(locs)

	def return_hand(self, num_tiles=7):
		return self.bag.pull_tiles(num_tiles)
	# 	hand = random.choice(self.bag.tiles, 7, replace = False)

	# 	return hand

	def print_hand(self, hand):
		out_str = ("| %s |" % " | ".join([tile.letter for tile in hand]))
		border = ("-" * len(out_str))
		print("\n".join([border, out_str, border]))

	def get_dictnode(self, word, _dict = None):# self.dictionary):
			"""Gets the from a valid first portion of a word in a dictionary"""
			node = self.dictionary if _dict == None else _dict
			try:
				for letter in word:
					node = node[letter]

			except KeyError as key_err:
				#print(key_err)
				#print("%s not in dictionary" % word)
				return {}

			return node


	def print_board(self):
		self.board.print_grid()

def NotEnoughTilesError(GameError):
	def __init__(self, expression, message):
		self.message = "Too few tiles to swap"

class Bag(object):
	def __init__(self, game):
		self.game = game
		self.tiles = []
		for letter, points, amount in consts.letter_points_amount:
			for _ in range(amount):
				self.tiles.append(Tile(game = self.game, letter = letter, points = points))

		random.shuffle(self.tiles)

	def pull_tiles(self, num_tiles = 1):
		pulled_tiles, self.tiles = (self.tiles[:num_tiles], self.tiles[num_tiles:])
		return pulled_tiles

	def swap_tiles(self, tiles_to_swap):
		"""Given a list of tiles to swap, gets the same number of tiles from the bag"""
		
		if len(self) < 7:
			raise NotEnoughTilesError

		new_tiles = self.pull_tiles(len(tiles_to_swap))
		self.tiles.extend(tiles_to_swap)
		return new_tiles

	def __len__(self):
		return len(self.tiles)

class Tile(object):
	def __init__(self, game, letter, points):
		self.game = game
		self.letter = letter
		self.points = points

	def __repr__(self):
		return self.letter

	
def gui_test():
	import tkinter as tk

	a = S_Board()
	top = tk.Tk()
	w = Canvas(top, bg = 'white', width = 225, height = 225)
	bonusGuide = {
				None:'white',
				'L2':'Cyan',
				'W2':'Pink',
				'L3':'Blue',
				'W3':'Red'}

	for r in range(15):
		for c in range(15):
			coords = [((r + a) * 15,(c + b) * 15) for a,b in [(0,0),(0,1),(1,1),(1,0)]]
			square = w.create_polygon(coords, fill = bonusGuide.get(a.grid[r][c].bonusType,'white'))

	w.pack()
	top.mainloop()

def main():
	game = Scrabble()
	game.print_board()


if __name__ == "__main__":
	main()