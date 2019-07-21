class Board:

    """docstring for S_Board"""
    def __init__(self, game):
        self.game = game

        _TWS = [(x,y) for x in [0,7,14] for y in [0,7,14]]
        _TWS.remove((7,7))
        _DWS = [(7 + dx*ffset,7+dy*ffset) for ffset in range(3,7) for dx in [-1,1] for dy in [-1,1]] 
        _DWS.append((7,7))

        # Double letters

        _DLS = [(x0+dx*mx,y0+dy*my)
                for x0,dx in [(0,1),(14,-1)] 
                    for y0,dy in [(0,1),(14,-1)]
                        for mx,my in [(0,3),(2,6),(3,7),(6,6),(3,0),(6,2),(7,3)]]

        # Triple letters
        _TLS = [(x0+dx*mx,y0+dy*my) 
                for x0,dx in [(0,1),(14,-1)]
                    for y0,dy in [(0,1),(14,-1)]
                        for mx,my in [(5,1),(5,5),(1,5)]]

        self.grid = [[Board_Space(self.game, self, (r, c), None) for r in range(15)] for c in range(15)]
        self.vert_grid = [[self.grid[c][r] for r in range(15)] for c in range(15)]
        _bonusType = None
        
        for coords_lst, poss_bonus in [(_DLS,"L2"),(_DWS,"W2"),(_TWS,"W3"),(_TLS,"L3")]:
            for coords in coords_lst:
                self[coords].set_bonus(poss_bonus)


    def place_tile_on_board(self, tile, coords):
        self[coords].place_tile_on_space(tile)

    def __getitem__(self, r, c = None):
        if c is None:
            if isinstance(r, int):
                return self.grid[r]
            r, c = r            
        return self.grid[r][c]

    def __setitem__(self, ind, value):
        self.place_tile_on_board(value, ind)

    def __repr__(self):
        result = ""
        result += ("_" * 76) + '\n'
        for row in self.grid:
            for printedRowFn in [
                    lambda tile: "   ",
                    lambda tile:
                        (" %s " % tile.tile.letter) if tile.occupied 
                        else 
                            tile.printedBonusType if tile.bonusType is not None 
                            else 
                                "   ",
                     lambda tile: "___"]:

                result += ("|%s|\n" % "|".join(map(printedRowFn, row)))
        return result

    def get(self, r,c = None):
        if c == None:
            r,c = r
        return self.grid[r][c]

    def get_letter(self, r,c = None):
        try:
            self[r, c].tile.letter
        except AttributeError:
            return 

    def score_word(self, new_tile_locs_preprocess):
        for r, c in new_tile_locs_preprocess:
            assert self[r][c].occupied

        rows, cols = zip(*new_tile_locs_preprocess)

        # Handle transposition of board if the word was placed vertically -------------------

        if len(set(rows)) == 1:
            board = self.grid
            new_tile_locs = new_tile_locs_preprocess
        else:
            assert len(set(cols)) == 1
            board = list(zip(*self.grid))
            new_tile_locs = [(a, b) for b, a in new_tile_locs_preprocess]

        main_word_score = 0
        r,original_c = new_tile_locs[0]

        # Scores a single word based on the word locations -----------------

        def score_single_word(word_locs):
            word_points = 0
            word_mult = 1

            for r, c in word_locs:
                space = board[r][c]
                tile = space.tile
                letter_mult = 1

                # Apply bonus
                if (r, c) in new_tile_locs:
                    word_mult *= space.wordBonus
                    letter_mult *= space.letterBonus

                word_points += letter_mult * tile.points

            return word_mult * word_points

        # --------- Find beginning and end of horizontal word ------------

        c = original_c
        letter = board[r][c].get_letter()

        while c >= 0 and letter is not None:
            c -= 1
            letter = board[r][c].get_letter()

        begin = c + 1

        c = original_c

        letter = board[r][c].get_letter()
        while c < 15 and letter is not None:
            c += 1
            letter = board[r][c].get_letter()

        end = c


        # --------- Get list of coordinates for each new word -----------
        main_word = [(r, curr_c) for curr_c in range(begin, end)]

        all_words = [main_word]
        for r, c in new_tile_locs:
            letter = board[r][c].get_letter()
            while r >= 0 and letter is not None:
                r -= 1
                letter = board[r][c].get_letter()
                
            r += 1
            letter = board[r][c].get_letter()

            curr_word_locs = list()

            while r < 15 and letter is not None:
                curr_word_locs.append((r, c))
                r += 1
                letter = board[r][c].get_letter()

            all_words.append(curr_word_locs)



        # -------- Return the score of each word with length > 1 ---------
        base_score = sum([score_single_word(word) for word in all_words if len(word) > 1])
        bonus_score = 50 if len(new_tile_locs) == 7 else 0
        return base_score + bonus_score



class Board_Space(object):

    def __init__(self, game, grid,loc, bonusType = None):
        """Makes a board space, taking the game
        , grid, its own location and a bonus type if it is a bonus tile"""
        self.game = game
        self.occupied = False
        self.tile = None
        self.bonusType = bonusType
        self.printedBonusType = ("%sx%s" % (bonusType[0],bonusType[1]) if self.bonusType is not None else "  ")

        if loc == (7,7):
            self.printedBonusType = " * "
        self.loc = loc
        self.grid = grid        
        self.in_range = lambda a: 0 <= a[0] < 15 and 0 <= a[1] < 15
        self.connectors = list(filter(self.in_range,
                                [(loc[0]+dr,loc[1]+dc)
                                    for dr in [-1,1]
                                        for dc in [-1,1]]))

        #Parsing bonus amount
        self.wordBonus = 1 
        self.letterBonus = 1

    def get_letter(self):
        if not self.occupied:
            return None

        else:
            return self.tile.letter

    def set_bonus(self, bonusType):
        self.bonusType = bonusType
        if(bonusType != None):
            bonusAmt = int(bonusType[1])
            if(bonusType [0] == "L"):
                self.letterBonus = bonusAmt
            else:
                self.wordBonus = bonusAmt

    def place_tile_on_space(self, tile):
        if(self.occupied or self.tile):
            raise OccupiedSpaceError
        self.occupied = True
        self.tile = tile

    def pick_up_tile(self):
        """ Remove and return tile"""
        tile = self.tile
        self.occupied = False
        self.tile = None
        return tile

    def __repr__(self):
        return ' ' if self.tile == None else self.tile.letter

