"""Brute force best starter word"""

from functools import reduce
import numpy as np
from S_Board import Scrabble

def score_firstword(tiles):
	_len = len(tiles)
	bonus_score = 0

	if _len >= 5:
		#Getting list of all the tiles that could be on the double
		#letter score, seeing which one has the most points, and adding that many points to total
		bonus_score += max([tile._points for tile in tiles[:_len - 4] + tiles[4 - _len:]])
		
	return ((bonus_score + sum(_tile._points for _tile in tiles)) * 2) + (50 if len(tiles) == 7 else 0)

def brute_force(dict_start, tiles):
	""" returns a word + score pair of the highest scoring word that can be made with the 7 tiles (assuming it's the first word)"""

	curr_words = [[]] if '$' in dict_start else []
	if(len(tiles) == 0):
		return curr_words

	best_score = 0
	can_advance = lambda tile, _dict: tile._letter in _dict

	letters_left = [tile._letter for tile in tiles]

	for idx, tile in enumerate(tiles):

		# Next letter is in the dictionary and the tile hasn't already been checked
		if tile._letter in dict_start and (idx == 0 or tile._letter not in [prev._letter for prev in tiles[:idx]]):

			# welcome to python where this constructs a list of all remaining tiles.
			remaining_tiles = [_tile for _tile in tiles if _tile is not tile]
			
			#Recursive call
			best_possible_followers = brute_force(dict_start[tile._letter], remaining_tiles)

			#If there was a word
			if len(best_possible_followers) > 0:

				local_max_hands = [([tile] + follower if follower != [] else [tile]) for follower in best_possible_followers]
				for hand in local_max_hands:
					if len(hand) == 7:
						print('Found bingo: %s' % ''.join([t._letter for t in hand]))

				curr_score = score_firstword(local_max_hands[0])

				if curr_score >= best_score:
					if curr_score > best_score:
						curr_words = []
					curr_words += local_max_hands
					best_score = curr_score


	return curr_words

def bruteforce_test(game):
	hand = game.return_hand()
	game.print_hand(hand)
	best_words = brute_force(game._dictionary, hand)
	# print(best_words)
	#for word in best_words:
	print ("Best word%s: %s (%d points)." % (
		"s" if len(best_words) > 1 else "",
		",".join(["".join([tile._letter for tile in word]) for word in best_words]),
		score_firstword(best_words[0])))
	# print("Best words: %s - %d points." % (", ".join([tile._letter for best_word in best_words for tile in best_word]), score_firstword(best_word)))

def main():
	a = Scrabble()
	bruteforce_test(a)

	



if __name__ == '__main__':
	main()
