"""Brute force best starter word"""

from functools import reduce
import numpy as np
from S_Board import Scrabble

def score_firstword(tiles):
	return (sum(_tile._points for _tile in tiles) * 2) + (50 if len(tiles) == 7 else 0)

def brute_force(dict_start, tiles):
	""" returns a word + score pair of the highest scoring word that can be made with the 7 tiles (assuming it's the first word)"""
	if(len(tiles) == 0):
		print("empty tiles list")
		return []

	best_score = 0
	curr_word = ([] if '$' in dict_start else None)
	can_advance = lambda tile, _dict: tile._letter in _dict

	letters_left = [tile._letter for tile in tiles]

	for idx, tile in enumerate(tiles):
		if tile._letter in dict_start:
			new_list = [_tile for _tile in tiles if _tile is not tile]
			
			best_possible_follower = brute_force(dict_start[tile._letter], new_list)

			if best_possible_follower is not None:
				local_max_hand = [tile] + best_possible_follower
				curr_score = score_firstword(local_max_hand)

				if curr_score > best_score:
					best_score = curr_score
					curr_word = local_max_hand

	return curr_word

def bruteforce_test(game)
	hand = game.return_hand()
	best_word = brute_force(game._dictionary, hand)
	print("Best word: %s - %d points." % ("".join([tile._letter for tile in best_word], score_firstword(best_word))))

def main():
	a = Scrabble()

	



if __name__ == '__main__':
	main()
