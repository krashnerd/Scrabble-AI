import Scrabble, bruteforcer, utils
import unittest
from string import ascii_uppercase

blank_board = ['_' * 15] * 15
verbose = True

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

def prettyprint(g):
	grid = [x if isinstance(x, str) else "".join(list(x)) for x in g]
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
				new_tile = Scrabble.Tile(game, letter)
				board[r_ind, c_ind] = new_tile

	return game

def cramp_game():
	letter_placements = blank_board[:]
	letter_placements[7] = add_padding(6, 'CR_MP')
	letter_placements = utils.grid_transpose(letter_placements)
	return game_from_string(letter_placements)


class ScoringTester(unittest.TestCase):
	def set_current_rack(self, game, letters):
		game.current_player.rack.clear()
		game.current_player.rack.extend([Scrabble.Tile(game, x) for x in letters])

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

	def validate_regex(self, regex, matchall = False, valid = [], invalid = []):

		self.assertEqual(matchall, utils.matches_all(regex))

		for valid_letter in valid:
			self.assertTrue(regex.match(valid_letter))

		for invalid_letter in invalid:
			self.assertFalse(regex.match(invalid_letter))


	def test_regex_suffix(self):
		letter_placements = blank_board[:]
		letter_placements[7] = add_padding(6, 'MAN')
		letter_placements = utils.grid_transpose(letter_placements)

		game = game_from_string(letter_placements)
		regs = bruteforcer.make_regexes(game, 9)
		test_row = 7

		# Testing to be sure it isn't an instance of re.compile('.')
		regex = regs[7]
		self.validate_regex(regex, matchall = False, valid = 'AESY', invalid = "LPUFZ")

	def test_regex_prefix(self):
		letter_placements = blank_board[:]
		letter_placements[7] = add_padding(6, 'RAMP')
		letter_placements = utils.grid_transpose(letter_placements)
		# prettyprint(letter_placements)

		game = game_from_string(letter_placements)
		regs = bruteforcer.make_regexes(game, 5)
		regex = regs[7]
		# Testing to be sure it isn't an instance of re.compile('.')
		self.validate_regex(regex, matchall = False, valid = "CT", invalid = "BDRFLP")

	def test_regex_infix(self):
		game = cramp_game()
		# prettyprint(letter_placements)
		test_row = 8

		# print(game.board)
		regs = bruteforcer.make_regexes(game, 8)
		regex = regs[7]
		one_non_matches_all = False
		for reg in regs:
			if not reg.match('0'):
				one_non_matches_all = True

		self.assertTrue(one_non_matches_all)

		# Testing to be sure it isn't an instance of re.compile('.')
		self.validate_regex(regex, matchall = False, valid = "AIU", invalid = "ZXCVBNM")

	def test_get_all_finds_legal_only(self):
		game = cramp_game()

		loc = (8, 7)

		game.current_player.rack.extend([Scrabble.Tile(game, x) for x in "LOOPERS"])
		all_moves = bruteforcer.get_all_row(game, 8, game.current_player.rack)
		for move in all_moves:
			applied = game.apply_move(move)
			self.assertTrue(applied.board[loc].occupied)
			self.assertTrue(applied.board[loc].letter in "AIU")

	def test_word_endpoints_cramp(self):
		"""Seeing if word_endpoints indeed returns what it should"""
		game = cramp_game()
		game.board.transpose()
		row = 7
		restrictions = bruteforcer.make_regexes(game, row)
		endpoints = bruteforcer.word_endpoints(game, row, restrictions)
		found = False
		self.assertTrue((6, 10) in endpoints)

	def test_get_all_finds_one_letter_plays(self):
		"""Testing to see if all_moves finds one-letter plays"""
		game = cramp_game()

		self.set_current_rack(game, "ABCDEFG")
		moves = [move for move in bruteforcer.all_moves(game)]
		if verbose:
			print(game.board)
			for move in moves:
				if len(move) == 1:
					print(move)
		self.assertTrue(1 in list(map(len, moves)))
		
		# Testing to see if it finds putting the 'A' in the middle of the word
		self.assertTrue([(tile, loc) for move in moves for tile, loc in move if len(move) == 1 and tile.letter == 'A' and loc == (8,7)])



	def test_highest_scoring_move_empty_board(self):
		"""Test to see if the brute forcer can find the highet-scoring move on an empty board"""
		game = game_from_string(blank_board)
		game.current_player.rack.extend([Scrabble.Tile(game, x) for x in "LOOPERS"])
		move = bruteforcer.highest_scoring_move(game)
		applied = game.apply_move(move)
		self.assertEqual(applied.last_move_score, 74)



	
















if __name__ == '__main__':

	unittest.main()



