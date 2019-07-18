import Scrabble, bruteforcer
import unittest
from string import ascii_uppercase

blank_board = ['_' * 15] * 15

def add_padding(*args):
	lst = list(args[:])
	for i, num in enumerate(lst):
		if isinstance(num, int):
			lst[i] = '_' * num
	return '{message:{fill}{align}{width}}'.format(
		message = ''.join(lst),
		fill = '_',
		align = '<',
		width = 15)

def prettyprint(grid):
	print("\n{}".format("\n".join(['{message:{fill}{align}{width}}'.format(
		message = '{}: {}'.format(str(index), row),
		fill = ' ',
		align = '>',
		width = 20) for index, row in enumerate(grid)])))



def string_grid_transpose(rows):
	return list(zip(*[list(row) for row in rows]))	

def game_from_string(letter_placements):
	game = Scrabble.Scrabble()
	board = game.board
	for r_ind, r_val in enumerate(letter_placements):
		for c_ind, letter in enumerate(r_val):
			if letter in ascii_uppercase:
				new_tile = Scrabble.Tile(game, letter, game.points[letter])
				board[r_ind, c_ind] = new_tile

	return game

class ScoringTester(unittest.TestCase):
	def test_basic_row(self):
		letter_placements = blank_board[:]
		letter_placements[0] = add_padding(4, 'AAA')
		new_tiles = [(0, x) for x in range(4, 7)]
		game = game_from_string(letter_placements)

		self.assertEqual(game.score_word(new_tiles), 3)

	def test_basic_col(self):
		letters = string_grid_transpose([add_padding(4, 'AAA')])

		new_tiles = [(x, 0) for x in range(4, 7)]
		game = game_from_string(letters)
		self.assertEqual(game.score_word(new_tiles), 3)

	def test_bonuses(self):
		letter_placements = blank_board[:]
		letter_placements[7] = add_padding(6, 'AAAAAAAA')
		new_tiles = [(7, x) for x in range(7, 10)]
		game = game_from_string(letter_placements)
		self.assertEqual(game.score_word(new_tiles), 16)

		new_tiles = [(7, x) for x in range(6, 14)]
		self.assertEqual(game.score_word(new_tiles), 18)

	def test_compound_words(self):
		letter_placements = blank_board[:]

		letter_placements[6] = add_padding(7, "AA")
		letter_placements[7] = add_padding(7, "AAA")
		game = game_from_string(letter_placements)
		new_tiles = [(6,7),(6,8)]

		self.assertEqual(game.score_word(new_tiles), 8)

	def test_regex_basic(self):
		letter_placements = blank_board[:]
		letter_placements[7] = add_padding(6, 'MAN')
		prettyprint(["".join(x) for x in zip(*list(map(list, letter_placements)))])

		game = game_from_string(letter_placements)
		re = bruteforcer.make_regexes(game, 9)
		for valid in 'EY':
			pass















if __name__ == '__main__':

	unittest.main()



