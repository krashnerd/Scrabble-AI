import Scrabble, bruteforcer
import unittest
from string import ascii_uppercase

blank_board = ['_' * 15] * 15

def add_padding(lst):
	for i, num in enumerate(lst):
		if isinstance(num, int):
			lst[i] = '_' * num
	return '{message:{fill}{align}{width}}'.format(
		message = ''.join(lst),
		fill = '_',
		align = '<',
		width = 15)

def string_grid_transpose(rows):
	return list(zip(*[row.split('') for row in rows]))	

def game_from_string(letter_placements):
	game = Scrabble.Scrabble()
	board = game.board
	for r_ind, r_val in enumerate(letter_placements):
		for c_ind, letter in enumerate(r_val):
			if letter in ascii_uppercase:
				new_tile = Scrabble.Tile(game, letter, game.points[letter])
				board[r, c] = new_tile

	return game

class ScoringTester(unittest.TestCase):
	def basic_row_test(self):
		board = blank_board[:]
		board[0] = add_padding(4, 'AAA')
		new_tiles = [(0, x) for x in range(4, 7)]
		game = game_from_string(letter_placements)
		self.assertEqual(board.score_word(new_tiles), 3)

	def basic_col_test(self):
		letters = string_grid_transpose(add_padding(4, 'AAA'))

		new_tiles = [(x, 0) for x in range(4, 7)]
		game = game_from_string(letters)
		self.assertEqual(board.score_word(new_tiles), 3)







if __name__ == '__main__':
	unittest.main()



