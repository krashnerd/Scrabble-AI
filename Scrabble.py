import build_dictionary
from numpy import random
from Board import Board
class Scrabble(object):
	def __init__(self):
		self.bag = Bag(self)
		self.board = Board(self)
		self.dictionary = build_dictionary.get_dawg("dictionary/dictionary.json")
		self.check_word = lambda word:build_dictionary.check_word(word, self.dictionary)
		points = {1:"AEIOULNSTR",2:"DG",3:"BCMP",4:"FHVWY",5:"K",8:"JX",10:"QZ"}
		self.points = dict()
		for num, letters in list(points):
			for letter in letters:
				self.points[letter] = num

		
		dist = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]





	def score(word):
		points = 0
		for tile in word:
			points += tile.points * 2
		if len(word) == 7:
			points += 50
		return points

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

class Bag(object):
	def __init__(self, game):
		self.game = game
		self.tiles = []
		points = {1:"AEIOULNSTR",2:"DG",3:"BCMP",4:"FHVWY",5:"K",8:"JX",10:"QZ"}

		for pointVal in points.keys():
			for letter in points[pointVal]:
				letter_amt = dist[ord(letter) - ord("A")]
				for i in range(letter_amt):
					self.tiles.append(Tile(self.game, letter, pointVal))
		random.shuffle(self.tiles)

	def pull_tiles(self, num_tiles = 1):
		pulled_tiles, self.tiles = (self.tiles[:num_tiles], self.tiles[num_tiles:])
		return pulled_tiles

	def swap_tiles(self, tiles_to_swap):
		"""Given a list of tiles to swap, gets the same number of tiles from the bag"""

		new_tiles = self.pull_tiles(len(tiles_to_swap))
		self.tiles += tiles_to_swap
		return new_tiles

class Tile(object):
	def __init__(self, game, letter, points):
		self.game = game
		self.points = points
		self.letter = letter

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