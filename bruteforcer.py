"""Brute force best starter word"""
import csv, string
from functools import reduce
import numpy as np
from Scrabble import Scrabble

def score_firstword(tiles):
    _len = len(tiles)
    bonus_score = 0

    if _len >= 5:
        #Getting list of all the tiles that could be on the double
        #letter score, seeing which one has the most points, and adding that many points to total
        bonus_score += max([tile.points for tile in tiles[:_len - 4] + tiles[4 - _len:]])
        
    return ((bonus_score + sum(_tile.points for _tile in tiles)) * 2) + (50 if len(tiles) == 7 else 0)

def get_letters_row(coords, game):
    """ Given a coordinate, find what letters 
    can be put in said coordinate assuming that only one letter is going in the column
    (word is being placed horizontally)"""
    board = game.board

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

    return "[{}]".format(possible)

def make_regex(game, row_ind):
    """List of regexes for each square in the row, restricting based on the column"""
    possibilities = [[] for _ in range(15)]
    board = game.board
    for col_ind in range(15):
        space = board.get(row_ind, col_ind)
        if space.occupied:
            possibilities[col_ind] = [space.tile.letter]
        else:
            possibilities[col_ind] = get_letters_row((row_ind, col_ind), game)

    return possibilities

def word_endpoints(game, row_ind, restrictions_list, tiles = None):
    """Given a certain row in a certain game, as well as
    the regex for how spaces are limited by the columns, determine all possible starts and ends.
    Determines the start and end of the actual word, not the start and end of where tiles would be placed, 
    so if the placement would be a suffix, for example if the row contained the word "WORLD", 
    and the move would just be to place an S on the end, the start point would be the location of the W, not the location of the S
    """

    occupied_spaces = set([c for c in range(15) if game.board.get(row_ind, c).occupied])

    bordering_spaces = set([c for c in range(15)
        if (restrictions_list[c] != '.') or
            ({c + 1, c - 1} & occupied_spaces)]) -
            occupied_spaces

    unplayable = set([c for c in range(15) if restrictions_list[c] == "[]"])

    # Count the starting square as a bordering space.
    if row_ind == 7 and occupied_spaces == set():
        bordering_spaces.add(7)

    empty_spaces = set([a for a in range(15)]) - occupied_spaces

    pairs = []
    for start in range(15):
        if (start - 1) in occupied_spaces:
            continue

        for end in range(start, 15):
            if (end + 1) in occupied_spaces:
                continue

            wordrange = set([i for i in range(start, end)])
            if len(wordrange & empty_spaces) > 7:
                continue

            if wordrange & bordering_spaces:
                pairs.append(start, end)

    return pairs



def get_all(game, row, letters):
    """Get all possible moves with a given row and set of letters"""
    poss_letters = make_regex(game, row)
    endpoint_pairs = word_endpoints(game, row, poss_letters)
    board = game.board
    for start, end in endpoint_pairs: 
        tiles_remaining = tiles[:]
        dict_node = game.dictionary

        def search_moves_rec(curr_loc = (row, start), curr_dict = game.dict, tiles_left = tiles[:]):
            curr_letter = game.board[*curr_loc].get_letter()
            results = []
            if curr_letter is None:
                for tile in tiles_left:
                    if tile.letter in curr_dict:
                        removed = [x for x in tiles if x is not tile]
                        results.concat(search_moves_recursive)


            


    for c in range(*endpoints):




        curr_tile = 

        for idx, tile in enumerate(tiles):

            # Next letter is in the dictionary and the tile hasn't already been checked
            if tile.letter in dict_start and (idx == 0 or tile.letter not in [prev.letter for prev in tiles[:idx]]):

                # list of all remaining tiles.
                remaining_tiles = [_tile for _tile in tiles if _tile is not tile]
                
                #Recursive call
                best_possible_followers = brute_force(dict_start[tile.letter], remaining_tiles)

                #If there was a word
                if len(best_possible_followers) > 0:

                    local_max_hands = [([tile] + follower if follower != [] else [tile]) for follower in best_possible_followers]
                    # for hand in local_max_hands:
                    #   if len(hand) == 7:
                    #       print('Found bingo: %s' % ''.join([t.letter for t in hand]))

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
    can_advance = lambda tile, _dict: tile.letter in _dict

    letters_left = [tile.letter for tile in tiles]

    for idx, tile in enumerate(tiles):

        # Next letter is in the dictionary and the tile hasn't already been checked
        if tile.letter in dict_start and (idx == 0 or tile.letter not in [prev.letter for prev in tiles[:idx]]):

            # list of all remaining tiles.
            remaining_tiles = [_tile for _tile in tiles if _tile is not tile]
            
            #Recursive call
            best_possible_followers = brute_force(dict_start[tile.letter], remaining_tiles)

            #If there was a word
            if len(best_possible_followers) > 0:

                local_max_hands = [([tile] + follower if follower != [] else [tile]) for follower in best_possible_followers]
                # for hand in local_max_hands:
                #   if len(hand) == 7:
                #       print('Found bingo: %s' % ''.join([t.letter for t in hand]))

                curr_score = score_firstword(local_max_hands[0])

                if curr_score >= best_score:
                    if curr_score > best_score:
                        curr_words = []
                    curr_words += local_max_hands
                    best_score = curr_score


    return curr_words

def bruteforce_test(game):
    hand = game.return_hand()
    best_words = brute_force(game.dictionary, hand)
    # print(best_words)
    #for word in best_words:
    print ("Best word%s: %s (%d points)." % (
        "s" if len(best_words) > 1 else "",
        ",".join(["".join([tile.letter for tile in word]) for word in best_words]),
        score_firstword(best_words[0])))
    # print("Best words: %s - %d points." % (", ".join([tile.letter for best_word in best_words for tile in best_word]), score_firstword(best_word)))

def make_dataset():
    with open('starting_hands_training_data.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, quoting = csv.QUOTE_MINIMAL)
        for i in range(300000//14):
            game = Scrabble()
            for hand in range(12):
                hand = game.return_hand()
                best_words = brute_force(game.dictionary, hand)
                best_words.append([])
                csvwriter.writerow([''.join(sorted([tile.letter for tile in hand])), str(score_firstword(best_words[0]))])
        #print([''.join([tile.letter for tile in hand]),str(score_firstword(best_words[0]))])
            # print(best_words)
            #for word in best_words:
            
    # print("Best words: %s - %d points." % (", ".join([tile.letter for best_word in best_words for tile in best_word]), score_firstword(best_word)))


def main():
    a = Scrabble()
    make_dataset()



if __name__ == '__main__':
    main()
