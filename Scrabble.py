import json, string, copy
import consts


from numpy import random
from ScrabbleBoard import Board, InvalidMoveError
from ScrabbleTile import Tile
from ScrabbleDictionary import dictionary
from exceptions import *

# class Move():
# 	def __init__(self, start_loc, end_loc, word):
# 		self.start_loc = start_loc
# 		self.word = word

class Rack(list):
	def __init__(self, items = []):
		super().__init__(items)

	def has_tiles(self, move):
		for x in move:
			if isinstance(x, Tile):
				tile = x
			else:
				tile, _ = x
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
			self.remove(letter)
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
	def __init__(self):
		self.rack = Rack()
		self.score = 0



class Scrabble(object):
	""" Scrabble Game """
	def __init__(self, num_players = 2):
		self.letter_dist = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1]
		points = {1:"AEIOULNSTR",2:"DG",3:"BCMP",4:"FHVWY",5:"K",8:"JX",10:"QZ"}
		self.players = [InternalPlayer() for _ in range(num_players)]
		self.bag = Bag()
		self.board = Board()

		self.bingo_count = 0
		self.refill_racks()
		self.consecutive_passes = 0

		self.last_move_score = 0
		self.current_player_index = 0
		self.current_player = self.players[self.current_player_index]
		self.winner = None

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

	def refill_racks(self):
		for player in self.players:
			rack = player.rack
			rack.extend(self.bag.pull_tiles(rack.tiles_needed()))

	# def return_hand(self, num_tiles = 7):
	# 	return self.bag.pull_tiles(num_tiles)
	# # 	hand = random.choice(self.bag.tiles, 7, replace = False)

	# 	return hand

	def print_hand(self, hand):
		out_str = ("| %s |" % " | ".join([tile.letter for tile in hand]))
		border = ("-" * len(out_str))
		print("\n".join([border, out_str, border]))

	# def get_dictnode(self, word, _dict = None):# self.dictionary):
	# 		"""Gets the from a valid first portion of a word in a dictionary"""
	# 		node = self.dictionary if _dict == None else _dict
	# 		try:
	# 			for letter in word:
	# 				node = node[letter]

	# 		except KeyError as key_err:
	# 			#print(key_err)
	# 			#print("%s not in dictionary" % word)
	# 			return {}

	# 		return node

	def end_game(self):
		empty_rack_player = [player for player in self.players if not player.rack]
		if empty_rack_player:
			bonus_recipient = empty_rack_player[0]
			bonus_score = 0
						
			for player in self.players:
				penalty = sum(tile.points for tile in player.rack)
				bonus_recipient.score += penalty
				player.score -= penalty

		self.winner = max(enumerate(self.players), key = lambda x:x[1].score)[0]

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
		assert not self.board.is_transposed
		player = self.current_player

		if self.winner is not None:
			raise GameOverError

		try:
			new_locs = [loc for _, loc in move]
		except TypeError:
			player.rack.extend(self.bag.swap_tiles(move))
			
			for tile in move:
				player.rack.remove(tile)

			score = 0
			self.change_turn()
			return


		try:
			score = self.board.check_move_score(move)

		except EmptyMoveError:
			self.change_turn()
			return
			

		if len(move) == 7:
			self.bingo_count += 1

		# If every player passes their turn, end the game.
		self.consecutive_passes = 0 if move else self.consecutive_passes + 1
		if self.consecutive_passes >= len(self.players):
			self.end_game()
			return
		
		for tile, loc in move:
			self.board[loc] = tile
			player.rack.remove(tile)
		self.refill_racks()
		if not player.rack:
			self.end_game()

		player.score += score

		self.change_turn()
		self.last_move_score = score

	def test_move(self, move):
		return self.board.check_move_score(move)


def NotEnoughTilesError(GameError):
	def __init__(self, expression, message):
		self.message = "Too few tiles to swap"

class Bag(object):
	def __init__(self):
		self.tiles = []
		for letter, points, amount in consts.letter_points_amount:
			for tile_id in range(amount):
				self.tiles.append(Tile(letter = letter, points = points, tile_id = tile_id))

		self.all_tiles = self.tiles[:]

		random.shuffle(self.tiles)

	def pull_tiles(self, num_tiles = 1):
		pulled_tiles, self.tiles = (self.tiles[:num_tiles], self.tiles[num_tiles:])
		return pulled_tiles

	def isempty(self):
		return len(self) == 0

	def swap_tiles(self, tiles_to_swap):
		"""Given a list of tiles to swap, gets the same number of tiles from the bag"""
		
		if len(self) < 7:
			return tiles_to_swap

		new_tiles = self.pull_tiles(len(tiles_to_swap))
		self.tiles.extend(tiles_to_swap)
		return new_tiles

	def __len__(self):
		return len(self.tiles)

	def __iter__(self):
		for tile in self.tiles:
			yield tile

	
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