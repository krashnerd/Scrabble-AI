import json, string, copy
import build_dictionary, consts

from numpy import random
from Board import Board
from collections import OrderedDict

class GameError(Exception):
	pass

class TileNotFoundError(GameError):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		self.expression = expression
		self.message = "Tile not found in player rack"

# class Move():
# 	def __init__(self, start_loc, end_loc, word):
# 		self.start_loc = start_loc
# 		self.word = word

class Rack(list):
	def __init__(self, game, items = []):
		self.game = game
		super().__init__(items)

	def refill(self):
		self.extend(self.game.bag.pull_tiles(self.tiles_needed()))

	def has_tiles(self, move):
		for tile, position in move:
			if tile not in self:
				return False

		return True

	def remove_letter(self, letter):
		for tile in self:
			if tile.letter == letter:
				to_remove = tile
				break
		try:
			self.remove(to_remove)
		except UnboundLocalError:
			raise TileNotFoundError

	def remove_tiles(self, move):

		if isinstance(move, TileExchange):
			pass
		try:
			for tile, _ in move:
				self.remove(tile)
		
		except ValueError:
			raise TileNotFoundError

		else:
			self.refill()

	def tiles_needed(self):
		return 7 - len(self)


class InternalPlayer:
	def __init__(self, game = None):
		self.game = game
		self.rack = Rack(self.game)
		self.score = 0

class Scrabble(object):
	def __init__(self, num_players = 2):
		self.letter_dist = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]
		points = {1:"AEIOULNSTR",2:"DG",3:"BCMP",4:"FHVWY",5:"K",8:"JX",10:"QZ"}
		self.players = [InternalPlayer(self) for _ in range(num_players)]

		self.last_move_score = 0
		self.current_player_index = 0
		self.change_turn()
		self.winner = None
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
		if not locs:
			return 0
		return self.board.score_word(locs)

	def return_hand(self, num_tiles = 7):
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

	def end_game(self):
		best_score = max([player.score for player in self.players])
		for i, player in enumerate(self.players):
			print("Player {}: {}".format(i, player.score))
			if player.score == best_score:
				self.winner = i

	def get_winner(self):
		return self.winner



	def print_board(self):
		self.board.print_grid()

	def change_turn(self):
		self.current_player_index = (self.current_player_index + 1) % len(self.players)
		self.current_player = self.players[self.current_player_index]
		if self.current_player is None:
			self.change_turn()

	def apply_move(self, move):
		new = copy.deepcopy(self)
		new_locs = [loc for _, loc in move]
		player = new.current_player
		for tile, loc in move:
			new.board[loc] = tile
			player.rack.remove_letter(tile.letter)
		player.rack.refill()

		score = new.score_word(new_locs)
		player.score += score
		new.change_turn()
		new.last_move_score = score
		return new

	def test_move(self, move):
		return self.board.check_move_score(move)

	


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
		if not self.tiles:
			self.game.end_game()
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
	def __init__(self, game, letter, points = None):
		self.game = game
		self.letter = letter
		if points is not None:
			self.points = points
		else:
			_points, _ = consts.lookup_points_amount[letter]
			self.points = _points

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