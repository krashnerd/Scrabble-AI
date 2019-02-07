"""test_board.py

Testing for board"""
import random
from S_Board import Scrabble
import dawg_parser
def place_dummy_letter(board, letter, coords):
	game = board._game
	board.place_tile_on_board(game.Tile(game, letter, 1), coords)

def get_suffixes(game, prefix):
	node = game.get_dictnode(prefix)
	return "".join([letter for letter in node.keys() if '$' in node[letter]])

def in_range(coords, _len = 14):
	for coord in coords:
		if not (0 <= coord <= _len):
			return False
	return True

def put_dummy_word(board, word, start, _dir, _prefix = False):
	""" Place tiles for a word in the indicated direction,
	 starting from indicated point. 
	 Returns the coordinates of the next space."""

	r, c = start
	if(_prefix):
		r, c = (r + 1, c) if _dir[0].lower() == 'v' else (r, c + 1)
	for letter in word:
		if(r < 15 and c < 15):
			place_dummy_letter(board, letter, (r, c))
			r, c = (r + 1, c) if _dir[0].lower() == 'v' else (r, c + 1)
		else:
			return (-1, -1)
	return start if _prefix else (r,c)

def dict_get_prefixes(suffix, _dict):
	alpha = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.upper().split(' ')
	return [prefix for prefix in alpha if dawg_parser.check_word(suffix, _dict[prefix])]




def test_pure_prefix():
	alpha = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.upper().split(' ')
	suffixes = [word[1:] for word in 'windy, mat, seat, mate, wait, freeze'.upper().split(" ")] + alpha

	suffixes = ['Z']

	game = Scrabble()
	dictionary = game._dictionary
	passed = 0 	#tests passeed
	failed = 0
	tests = 0
	prefixes = alpha
	 	#tests run
	for suffix in suffixes:
		suffix_failed = []
		suffix_tests = 0
		suffix_passed = 0
		expected = dict_get_prefixes(suffix, dictionary)
		for coords in [(x,y) for x in range(4,5) for y in range(4,5)]:
			for _dir in 'v':
				h_board = game.Board(game)
				loc = put_dummy_word(h_board, suffix, coords, _dir, _prefix = True)
				print('coords: %s, loc: %s' % (str(coords), str(loc)))
				print(h_board)
				output = []

				if(in_range(loc)):
					suffix_tests += 1

					test_failed = False

					board_fn = h_board.get(loc).placeable_letters(scan_direction = 'v')

					for letter in alpha:
						if board_fn(letter):
							output.append(letter + suffix)

						if board_fn(letter) != letter in expected:

							suffix_failed.append((loc, _dir, letter))
							test_failed = True
							break

					print(output)

					if not test_failed:
						suffix_passed += 1
		suffix_failed_count = len(suffix_failed)
		print('Prefix: %s passed %d of %d tests' % (suffix, suffix_passed, suffix_tests))
		tests += suffix_tests
		passed += suffix_passed
		failed += suffix_failed_count


	print('TOTAL: %d of %d tests passed' % (passed, tests))




def test_pure_suffix():
	prefixes = 'ski hi abamper win pip stuc stin star fer cxa x p a b c d e f g h i j k l m n o p q r s t u v w x y z qu'.upper().split(" ")
	alpha = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.upper().split(' ')
	game = Scrabble()
	passed = 0 	#tests passeed
	failed = 0
	tests = 0
	 	#tests run
	for prefix in prefixes:
		prefix_failed = []
		prefix_tests = 0
		prefix_passed = 0
		expected = dict_get_suffix(prefix)
		for coords in [(x,y) for x in range(9) for y in range(9)]:
			for _dir in 'vh':
				h_board = game.Board(game)
				loc = put_dummy_word(h_board, prefix, coords, _dir)
				if(in_range(loc)):
					prefix_tests+= 1
					test_failed = False
					board_fn = h_board.get(loc).placeable_letters(_dir)
					for letter in alpha:
						if board_fn(letter) != letter in expected:
							prefix_failed.append((loc, _dir, letter))
							test_failed = True
							break
					if not test_failed:
						prefix_passed += 1
		prefix_failed_count = len(prefix_failed)
		print('Prefix: %s passed %d of %d tests' % (prefix, prefix_passed, prefix_tests))
		tests += prefix_tests
		passed += prefix_passed
		failed += prefix_failed_count


	print('TOTAL: %d of %d tests passed' % (passed, tests))








				

def dict_get_suffix(lst):
	lst = [word.upper() for word in lst.split(" ")]
	game = Scrabble()
	gw = lambda word: get_suffixes(game, word)
	return([letter + suf for letter in lst for suf in gw(letter)])


def main():
	test_pure_prefix()






if __name__ == '__main__':
	main()


