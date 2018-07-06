import dawg_parser
from numpy import random
class Scrabble(object):
	def __init__(self):
		self._bag = self.Bag(self)
		self._board = self.Board(self)
		self._dictionary = dawg_parser.get_dawg("full_output.json")
		self.check_word = lambda word:dawg_parser.check_word(word, self._dictionary)

	def score(word):
		points = 0
		for tile in word:
			points += tile._points * 2
		if len(word) == 7:
			points += 50
		return points

	def return_hand(self, num_tiles=7):
		return self._bag.pull_tiles(num_tiles)
	# 	hand = random.choice(self._bag._tiles, 7, replace = False)

	# 	return hand

	def print_hand(self, hand):
		out_str = ("| %s |" % " | ".join([tile._letter for tile in hand]))
		border = ("-" * len(out_str))
		print("\n".join([border, out_str, border]))

	def get_dictnode(self, word):
			""" Gets the node of a VALID word in the dictionary"""
			node = self._dictionary

			try:
				for letter in word:
					node = node[letter]

			except KeyError as key_err:
				print(key_err)
				print("%s not in dictionary" % word)
				return None

			return node






	def print_board(self):
		self._board.print_grid()

	class Bag(object):
		def __init__(self, game):
			self._game = game
			self._tiles = []
			dist = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]
			points = {1:"AEIOULNSTR",2:"DG",3:"BCMP",4:"FHVWY",5:"K",8:"JX",10:"QZ"}

			for pointVal in points.keys():
				for letter in points[pointVal]:
					letter_amt = dist[ord(letter) - ord("A")]
					for i in range(letter_amt):
						self._tiles.append(self._game.Tile(self._game, letter, pointVal))
			random.shuffle(self._tiles)

		def pull_tiles(self, num_tiles = 1):
			pulled_tiles, self._tiles = (self._tiles[:num_tiles], self._tiles[num_tiles:])
			return pulled_tiles

		def swap_tiles(self, tiles_to_swap):
			"""Given a list of tiles to swap, gets the same number of tiles from the bag"""

			new_tiles = self.pull_tiles(len(tiles_to_swap))
			self._tiles += tiles_to_swap
			return new_tiles

	class Tile(object):
		def __init__(self, game, letter, points):
			self._game = game
			self._points = points
			self._letter = letter

		def __repr__(self):
			return self._letter


	class player:
		pass

	class Board(object):

		"""docstring for S_Board"""
		def __init__(self, game):
			self._game = game

			_TWS = [(x,y) for x in [0,7,14] for y in [0,7,14]]
			_TWS.remove((7,7))
			_DWS = [(7 +dx*ffset,7+dy*ffset) for ffset in range(3,7) for dx in [-1,1] for dy in [-1,1]] 
			_DWS.append((7,7))

			_DLS = [(x0+dx*mx,y0+dy*my)
					for x0,dx in [(0,1),(14,-1)] 
						for y0,dy in [(0,1),(14,-1)]
							for mx,my in [(0,3),(2,6),(3,7),(6,6),(3,0),(6,2),(7,3)]]
			_TLS = [(x0+dx*mx,y0+dy*my) 
					for x0,dx in [(0,1),(14,-1)]
						for y0,dy in [(0,1),(14,-1)]
							for mx,my in [(5,1),(5,5),(1,5)]]

			self._grid = [[]] * 15
			for r in range(15):
				for c in range(15):
					_bonusType = None
					for pair in [(_DLS,"L2"),(_DWS,"W2"),(_TWS,"W3"),(_TLS,"L3")]:
						coord_list, poss_bonus = pair
						if (r, c) in coord_list:
							_bonusType = poss_bonus

					self._grid[r].append(self.Board_Space(self, self._game, (r, c), _bonusType))

		
		def print_grid(self):
			print("_" * 76)
			for row in self._grid:
				for printedRowFn in [
						lambda tile: "   ",
						lambda tile:
							(" %s " % tile._letter) if tile._occupied 
							else 
								tile._printedBonusType if tile._bonusType is not None 
								else 
									"   ",
						 lambda tile: "___"]:

					print("|%s|" % "|".join(map(printedRowFn, row)))

		def get(r,c):
			return self._grid[r][c]

		class Board_Space(object):


			def __init__(self, game ,grid,loc, bonusType = None):
				"""Makes a board space, taking the game
				, grid, its own location and a bonus type if it is a bonus tile"""
				self._game = game
				self._occupied = False
				self._letter = None
				self._bonusType = bonusType
				self._printedBonusType = ("%sx%s" % (bonusType[0],bonusType[1]) if self._bonusType is not None else "  ")

				if loc == (7,7):
					self._printedBonusType = " * "
				self._loc = loc
				self._grid = grid		
				self.in_range = lambda a: 0 <= a[0] < 15 and 0 <= a[1] < 15
				self._connectors = list(filter(self.in_range,
										[(loc[0]+dr,loc[1]+dc)
											for dr in [-1,1]
												for dc in [-1,1]]))

				#Parsing bonus amount
				self._wordBonus = 1 
				self._letterBonus = 1
				if(bonusType != None):
					bonusAmt = int(bonusType[1])
					if(bonusType [0] == "L"):
						self._letterBonus = bonusAmt
					else:
						self._wordBonus = bonusAmt

			def connector(self):
				if self._occupied:
					return False
				for connector in self._connectors:
					if(connector._occupied):
						return True

				return self._loc == (7,7)

			def placeable_letters(self, direction):
				"""Returns a function saying if a given letter can be placed as a suffix in a given direction"""
				dr, dc = (1, 0) if direction[0].lower() == "v" else (0, 1)

				prefix = ""
				curr_r, curr_c = self._loc
				for back_forth in [-1]:#, 1]:
					while True:
						curr_r, curr_c = (curr_r + (back_forth * dr), curr_c - (back_forth * dc))

						if not self.in_range(curr_r, curr_c):
							break

						curr = self._grid.get(curr_r, curr_c)
						
						if not curr._occupied:
							break

						{-1:prefix, 1:suffix}
						prefix = curr._letter + prefix

				if len(prefix) == 0:
					return lambda letter: True

				poss_suffixes_node = self._game.get_dictnode(prefix)				 

				valid_suffix_list = [suffix for suffix in poss_suffixes_node.keys() if '$' in poss_suffixes_node[suffix]]
				if len(valid_suffix_list) == 0:
					return lambda letter: False
				
				return lambda letter: letter in valid_suffix_list





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
			square = w.create_polygon(coords, fill = bonusGuide.get(a._grid[r][c]._bonusType,'white'))

	w.pack()
	top.mainloop()

def main():
	game = Scrabble()
	game.print_board()


if __name__ == "__main__":
	main()