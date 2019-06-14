"""Brute force best starter word"""
import csv, string
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

def score_horiz_word(game, new_tile_locs):
    main_word_score = 0
    r,c = new_tile_locs[0]
    

    for loc in new_tile_locs:



    



def make_regex(game, row_ind):
    """Creates a regular expression for the possible letters in each square of the row"""
    possibilities = [[] for _ in range(15)]
    board = game._board
    for col_ind in range(15):
        space = board.get(row_ind, col_ind)
        if space._occupied:
            possibilities[col_ind] = [space._tile._letter]
        else:
            possibilities[col_ind] = "[{}]".format(get_letters_row((row_ind, col_ind), game))
            

    

def word_endpoints(game, row_ind, restrictions_list):
    """Given a certain row in a certain game, as well as
    the regex for how spaces are limited by the columns, determine all possible starts and ends"""

    occupied_spaces = set([col_ind for col_ind in range(15) if game._board.get(row_ind, col_ind) is not None])

    bordering_spaces = set([col_ind for col_ind in range(15)
        if (restrictions_list[col_ind] != '.') or ({col_ind + 1, col_ind - 1} & occupied_spaces != set()) and
         col_ind not in occupied_spaces])

    # Count the starting square as a bordering space.
    if row_ind == 7 and occupied_spaces == set():
        bordering_spaces.add(7)

    empty_spaces = set([col_ind for col_ind in range(15) if col_ind not in (occupied_spaces + bordering_spaces)])

    pairs = []
    for start in range(15):
        for end in range(start, 15):
            wordrange = set([i for i in range(start, end)])
            if len(wordrange & empty_spaces) > 7:
                continue
            if (wordrange & (occupied_spaces|bordering_spaces)) == set():
                continue
            pairs.append(start, end)

    return pairs

def get_letters_row(coords, game):
    """ Given a coordinate, find what letters 
    can be put in said coordinate assuming that only one letter is going in the column
    (word is being placed horizontally)"""
    board = game._board

    r,c = coords
    letters = [board.get_letter(i, c) for i in range(15)]

    string = [("_" if letter is None else letter) for letter in letters]
    string[r] = "?"
    string = "".join(string)
    chunks = "_".split(string)

    # Get the 
    for possible_chunk in chunks:
        if "?" in possible_chunk:
            chunk = possible_chunk
            break

    if len(chunk) == 1:
        return '.'

    possible = ""
    for letter in string.ascii_uppercase:
        word = chunk.replace("?", letter)
        if game.check_word(word):
            possible += letter

    return possible

def get_all(game, row, letters):
    """Get all possible moves with a given row and set of letters"""
    poss_letters = make_regex(game, row)
    endpoint_pairs = word_endpoints(game, row, poss_letters)
    for start, end in endpoint_pairs: 


        for idx, tile in enumerate(tiles):

        # Next letter is in the dictionary and the tile hasn't already been checked
        if tile._letter in dict_start and (idx == 0 or tile._letter not in [prev._letter for prev in tiles[:idx]]):

            # list of all remaining tiles.
            remaining_tiles = [_tile for _tile in tiles if _tile is not tile]
            
            #Recursive call
            best_possible_followers = brute_force(dict_start[tile._letter], remaining_tiles)

            #If there was a word
            if len(best_possible_followers) > 0:

                local_max_hands = [([tile] + follower if follower != [] else [tile]) for follower in best_possible_followers]
                # for hand in local_max_hands:
                #   if len(hand) == 7:
                #       print('Found bingo: %s' % ''.join([t._letter for t in hand]))

                curr_score = score_firstword(local_max_hands[0])

                if curr_score >= best_score:
                    if curr_score > best_score:
                        curr_words = []
                    curr_words += local_max_hands
                    best_score = curr_score






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

            # list of all remaining tiles.
            remaining_tiles = [_tile for _tile in tiles if _tile is not tile]
            
            #Recursive call
            best_possible_followers = brute_force(dict_start[tile._letter], remaining_tiles)

            #If there was a word
            if len(best_possible_followers) > 0:

                local_max_hands = [([tile] + follower if follower != [] else [tile]) for follower in best_possible_followers]
                # for hand in local_max_hands:
                #   if len(hand) == 7:
                #       print('Found bingo: %s' % ''.join([t._letter for t in hand]))

                curr_score = score_firstword(local_max_hands[0])

                if curr_score >= best_score:
                    if curr_score > best_score:
                        curr_words = []
                    curr_words += local_max_hands
                    best_score = curr_score


    return curr_words

def bruteforce_test(game):
    hand = game.return_hand()
    best_words = brute_force(game._dictionary, hand)
    # print(best_words)
    #for word in best_words:
    print ("Best word%s: %s (%d points)." % (
        "s" if len(best_words) > 1 else "",
        ",".join(["".join([tile._letter for tile in word]) for word in best_words]),
        score_firstword(best_words[0])))
    # print("Best words: %s - %d points." % (", ".join([tile._letter for best_word in best_words for tile in best_word]), score_firstword(best_word)))

def make_dataset():
    with open('starting_hands_training_data.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, quoting = csv.QUOTE_MINIMAL)
        for i in range(300000//14):
            game = Scrabble()
            for hand in range(12):
                hand = game.return_hand()
                best_words = brute_force(game._dictionary, hand)
                best_words.append([])
                csvwriter.writerow([''.join(sorted([tile._letter for tile in hand])), str(score_firstword(best_words[0]))])
        #print([''.join([tile._letter for tile in hand]),str(score_firstword(best_words[0]))])
            # print(best_words)
            #for word in best_words:
            
    # print("Best words: %s - %d points." % (", ".join([tile._letter for best_word in best_words for tile in best_word]), score_firstword(best_word)))


def main():
    a = Scrabble()
    make_dataset()



if __name__ == '__main__':
    main()
