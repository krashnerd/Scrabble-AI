def get_start_of_word(grid, start_loc, direction = 1):

    loc = list(start_loc)
    letter = board[loc].get_letter()

    while loc[direction] >= 0 and letter is not None:
        loc[direction] -= 1
        letter = board[loc].get_letter()

    loc[direction] += 1

    return loc

def grid_transpose(grid):
    return list(zip(*[list(x) for x in grid]))

def matches_all(regex):
    return bool(regex.match('0'))

def count(iter):
    try:
        return len(iter)
    except TypeError:
        return sum(1 for _ in iter)



def validate_placement(single_placement):
    tile, loc = single_placement
    try:
        x, y = loc

       
        

    except TypeError:
        return False

    else:
         # Note: Sacrificing slight runtime efficiency for readability.
        return x in range(15) and y in range(15)