"""Brute force best starter word"""
import csv, string, re, utils
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

def get_tile_regex(coords, game, verbose = False):
    """ Given a coordinate, find what letters 
    can be put in said coordinate assuming that only one letter is going in the column
    (word is being placed horizontally)"""

    matchall = re.compile(".")
    board = game.board
    r,c = coords

    letters = ["?" if i == r else board.get_letter(i, c) for i in range(15)]
    letters = "".join([letter if letter else '_' for letter in letters])
    # Splits into sections
    chunks = letters.split("_")
    if verbose:
        print(col, chunks)
        print(game.board)
    chunk = None
    # Get the 
    for possible_chunk in chunks:
        if "?" in possible_chunk:
            if verbose:
                    print(chunk)
            chunk = possible_chunk
            break

    if len(chunk) == 1:
        return matchall

    possible = ""
    for letter in string.ascii_uppercase:
        word = chunk.replace("?", letter)
        if game.check_word(word):
            possible += letter

    return re.compile("[m{}]".format(possible))

def make_regexes(game, row_ind, verbose = False):
    """List of regexes for each square in the row, restricting based on the column"""
    possibilities = ['' for _ in range(15)]
    board = game.board
    for col_ind in range(15):
        space = board.get(row_ind, col_ind)
        if space.occupied:
            possibilities[col_ind] = re.compile("[{}]".format(space.tile.letter))
        else:
            possibilities[col_ind] = get_tile_regex((row_ind, col_ind), game, verbose)

    return possibilities[:]

def word_endpoints(game, row_ind, restrictions_list, tiles = None, verbose = False):
    """Given a certain row in a certain game, as well as
    the regex for how spaces are limited by the columns, determine all possible starts and ends.
    Determines the start and end of the actual word, not the start and end of where tiles would be placed, 
    so if the placement would be a suffix, for example if the row contained the word "WORLD", 
    and the move would just be to place an S on the end, the start point would be the location of the W, not the location of the S
    """

    occupied_spaces = {c for c in range(15) if game.board.get(row_ind, c).occupied}
    empty_spaces = set(range(15)) - occupied_spaces


    # Squares which border a current tile. Every play must include at least one bordering space.

    bordering_spaces = {c for c in range(15)
        if (not utils.matches_all(restrictions_list[c])) or
            ({c + 1, c - 1} & occupied_spaces)} - occupied_spaces
    # Letters in rack
    letters = None if tiles is None else "".join([tile.letter for tile in tiles])

    # Spaces which the player cannot use.
    unplayable = {c for c in empty_spaces if letters and not restrictions_list[c].match(letters)}

    # Count the starting square as a bordering space.
    if row_ind == 7 and occupied_spaces == set():
        bordering_spaces.add(7)

    pairs = []
    for start in range(15):
        if start in occupied_spaces or start in unplayable:
            continue

        max_end = start

        for end in range(start, 15):

            # if (end + 1) in occupied_spaces:
            #     continue

            wordrange = set(range(start, end))

            if len(wordrange & empty_spaces) > 7 or unplayable & wordrange:
                break

            if end in bordering_spaces:
                pairs.append((start, end))
                break

            # if wordrange & bordering_spaces:
            #     must_hit = end - 1
            #     pairs.append((start, ))
            #     break

    return pairs

def get_all_row(game, row, tiles):
    """Get all possible moves with a given row and set of letters"""
    row_regexes = make_regexes(game, row)
    endpoint_pairs = word_endpoints(game, row, row_regexes, tiles)
    board = game.board

    def search_moves_rec(col, min_end, _dict = game.dictionary, tiles_left = tiles[:], word = "", move = []):
        """Backtracking search from a start point."""
         
        # Base case 1: End of column
        if col == 15:
            return move if '$' in _dict else []
        loc = (row, col)

        # Recursive case 1: Tile is occupied. Move to next.
        letter = game.board[loc].get_letter()
        if letter:
            if letter not in _dict:
                return []
            for recursive_move in search_moves_rec(col + 1, min_end, _dict[letter], tiles_left, word + letter, move):
                yield recursive_move
            return
 
        # Recursive case 2: Nonempty square
        results = []

        # If it's a complete word and some tiles have been played, add to the results list.
        if '$' in _dict and len(tiles_left) < len(tiles) and col > min_end:
            yield move

        for tile in tiles_left:
            letter = tile.letter
            # If possible word following, and the letter can be played:
            if letter in _dict and row_regexes[col].match(letter):
                
                new_tiles_left = [x for x in tiles_left if x is not tile]
                new_move = move + [(tile, board[loc].loc)]
                for recursive_move in (search_moves_rec(col + 1, min_end, _dict[letter], new_tiles_left, word + letter, new_move)):
                    yield recursive_move

    for (start, end) in endpoint_pairs:
        for move in search_moves_rec(start, end):
            yield move

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

def all_moves(game):
    orig = game.board.grid[:]
    transposed = utils.grid_transpose(orig)
    moves = []
    vertical = False
    for direction in ("horizontal", "vertical"):
        for row in range(15):
            for move in get_all_row(game, row, game.current_player.rack):
                game.board.grid = orig
                yield move
                if direction == "vertical":
                    game.board.grid = transposed
        game.board.transpose()

def highest_scoring_move(game):
    
    return max(all_moves(game), key = lambda move: game.test_move(move))

def main():
    a = Scrabble()
    make_dataset()



if __name__ == '__main__':
    main()
