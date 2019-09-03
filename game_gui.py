"""
Author: Krishna Kahn

GUI wrapper



"""

import tkinter as tk
from tkinter import N, S, E, W, NE, NW, SE, SW
import Scrabble, utils
from ScrabbleBoard import InvalidMoveError
import ScrabbleTile
from players import GreedyPlayer

tile_size = 40
tile_center = (tile_size//2, tile_size//2)
board_size = 15 * tile_size

mini_square = [(0,0),(0,1),(1,1),(1,0)]

leftclick = '<Button-1>'

human = "human"

class Display():
    """ Main display window for Scrabble game """
    def __init__(self, win, players = [human, GreedyPlayer()]):

        self.win = win

        self.players = players
        self.current_player_index = 0

        self.game = Scrabble.Scrabble(len(self.players))
        game = self.game
        self.win.geometry('1000x900+2000+50')

        # Create board, then tiles, then rack. Ordering matters so that tiles are visible above the board.
        self.board = DisplayBoard(self, self.game)
        self.board.create_board()

        self.tiles = {tile: DisplayTile(self, tile) for tile in game.bag.all_tiles}

        self.rack = DisplayRack(self, self.game)
      

        self.buttons = tk.Frame(self.win, height = 10, width = 600)
        self.buttons.grid(column = 0, pady = 5, columnspan = 15)

        cheatbutton = tk.Button(self.buttons, text="cheat", width=10, command=self.cheat)
        playbutton = tk.Button(self.buttons, text = "play", width = 10, command = self.submit_move)
        clearbutton = tk.Button(self.buttons, text = "clear", width = 10, command = self.sync_gui)
        swapbutton = tk.Button(self.buttons, text = "swap", width = 10, command = self.submit_swap)

        button_lst = [cheatbutton, playbutton, clearbutton, swapbutton]

        for i, button in enumerate(button_lst):
            button.grid(sticky = E, column = 3 * i, row = 0, columnspan = 2, padx = 3)
        self.win.bind('q', self.destroy)

        self.scoreboard = tk.Frame(self.win, width = 2, height = 2)
        self.scoreboard.grid(row = 1, column = 20, rowspan = 4, padx = 5)



        self.make_score_labels()
        self.sync_gui()

    def show_scores(self):
        self.score_label.destroy()
        self.make_score_labels()
        self.score_label.grid()

    def cheat(self):
        """ Show the highest scoring move """
        self.sync_gui()
        best_move = GreedyPlayer().get_move(self.game)
        print(best_move)
        for game_tile, loc in best_move:
            r, c = loc

            self.board.current_move[game_tile] = loc

            tile = self.tiles[game_tile]
            tile.grid(row = r, column = c, pady = 0)
            

    def increment_player(self):
        """ Change turns """
        self.current_player_index += 1
        self.current_player_index %= len(self.players)
        self.current_player = self.players[self.current_player_index]


    
    def make_score_labels(self):
        """ SCoreboard update helper """
        scoreboard_text = "\n".join(str(player.score) for player in self.game.players)
        self.score_label = tk.Label(self.scoreboard, height = 0, text = scoreboard_text, font =("Arial", 50))

    def destroy(self, event):
        self.win.destroy()

    def submit_swap(self):
        """Swapping tiles"""
        move = self.board.current_move.keys()
        self.submit_move(move)

    def sync_gui(self):
        """Synchronize the gui to the current internal state of the game"""
        for r in range(15):
            for c in range(15):
                space = self.game.board[r, c]
                if space.occupied:
                    self.tiles[space.tile].grid(row = r, column = c, pady = 0)

        self.rack.refill_rack()
        self.show_scores()
        self.board.clear_move()
        

    def submit_move(self, move = None):
        move = move or self.board.current_move.items()
        if not move:
            return

        non_swaps = [x for x in move if not isinstance(x, ScrabbleTile.Tile)]

        if non_swaps:
            validated_move = list(filter(utils.validate_placement, move))
        else:
            validated_move = move

        try:
            self.game.apply_move(validated_move)
        except TypeError:
            print("Erroneous move:", validated_move)
            raise
        except InvalidMoveError:
            pass
        else:
            #If valid move, change current player and go

            placed_tiles = [self.tiles[tile] for tile, _ in validated_move] if non_swaps else validated_move

            for tile in placed_tiles:
                tile.placed = True

            self.increment_player()
            if self.current_player is not human:
                move = self.current_player.get_move(game = self.game)
                self.submit_move(move)




        # Reset the move list

        self.sync_gui()
        
    def place_tile(tile, location):
        """ Move a tile to a given location"""
        pass

    def clear_move(self):
        self.board.clear_move()



class DisplayRack():
    """ Wrapper class for rack"""
    def __init__(self, display, game):
        self.display = display
        self.master = display.win
        self.game = game
        self.tiles = []
        self.tile_lookup = self.display.tiles

    def __iter__(self):
        for tile in self.tiles:
            yield tile

    def grid(self, *args, **kwargs):
        self.gui_obj.grid(*args, **kwargs)

    def handle_tile_click():
        pass

    def refill_rack(self):
        for tile in self.tiles:
            if not tile.placed:
                tile.grid_forget()
        self.tiles = [self.tile_lookup.get(tile) for tile in self.game.current_player.rack]
        self.render()
    def render(self):
        for ind, tile in enumerate(self):
            tile.grid(row = 16, column = 2 + ind, pady = 20)




class DisplayTile(tk.Canvas):
    def __init__(self, display, game_tile):
        self.display = display
        self.win = self.display.win
        self.game_tile = game_tile
        self.placed = False
        self.letter = game_tile.letter
        self.points = game_tile.points

        super().__init__(self.win, width = tile_size, height = tile_size)

        self.create_rectangle(0,0,tile_size,tile_size, fill = 'beige')
        self.create_text(tile_center, text = self.letter, font = ("Arial", 24))
        self.create_text((35, 35), text = str(self.points), font = ("Arial", 8))

        self.bind(leftclick, self.handle_click)

    def handle_click(self, event):
        if not self.placed:
            self.focus_set()

    def __eq__(self, other):
        return ((isinstance(other, DisplayTile) and self.game_tile == other.game_tile) or
            (isinstance(other, Scrabble.Tile) and self.game_tile == other))

class DisplayBoard():
    def __init__(self, display, game):
        self.display = display
        self.master = self.display.win
        self.game = game or Scrabble.Scrabble()
        self.game_board = self.game.board      
        self.squares = [[None] * 15 for _ in range(15)]
        self.current_move = dict()
        self.focus_tile = []

    def clear_move(self):
        self.current_move = dict()

    def move_tile(loc_1, loc_2):
        pass


    def swap_tiles_at(self, loc_1, loc_2):
        # self.move_tile(loc_1, loc_2)
        # self.move_tile(loc_2, loc_1)
        r1,c1 = loc_1
        r2,c2 = loc_2
        s1 = self.squares[r1][c1]
        s2 = self.squares[r2][c2]
        s1.grid(row = r2, column = c2)
        s2.grid(row = r1, column = c1)
        self.squares[r1][c1] = s2
        self.squares[r2][c2] = s1

    def handle_click(self, r, c):
        """ Handle click on the square at (r, c)"""
        current_move_locs = (loc for _, loc in self.current_move.items())
        if (r, c) in current_move_locs or self.game_board[r,c].occupied:
            return

        tile = self.master.focus_get()
        if not isinstance(tile, DisplayTile):
            return
            # self.squares[r][c].grid_forget()
        self.current_move[tile.game_tile] = (r, c)

        tile.grid(row = r, column = c, pady = 0)
        self.master.focus_set()

    def create_board(self):
        bonus_color_lookup = {
                    'L2':'Cyan',
                    'W2':'Pink',
                    'L3':'Blue',
                    'W3':'Red',
                    }
        bonus_text_lookup = {
                    'L2':'Double\nletter\nscore',
                    'W2':'Double\nword\nscore',
                    'L3':'Triple\nletter\nscore',
                    'W3':'Triple\nword\nscore',
                    }

        def get_click_function(x, y):
            def func(event):
                self.handle_click(x, y)
            return func

        for c in range(15):
            for r in range(15):
                tile = self.game_board[r,c]
                coords = [((r + a) * tile_size, (c + b) * tile_size) for a,b in mini_square]
                x, y = ((r + .5) * tile_size, (c + .5) * tile_size)
                bonus = tile.bonusType
                bg_color = bonus_color_lookup.get(bonus, 'white')
                text_color = "white" if bg_color in ("Blue", "Red") else "black"

                square = tk.Canvas(self.display.win, width = tile_size, height = tile_size, bg = bg_color, 
                    borderwidth = 1, relief = tk.RIDGE, 
                    highlightcolor = 'black', highlightbackground = 'black')

                func = get_click_function(r, c)

                square.bind(leftclick, func)

                bonus_text = bonus_text_lookup.get(bonus, None)
                if bonus_text:
                    text = square.create_text(tile_center, text = bonus_text, font = ("Arial", 10), fill = text_color, justify = tk.CENTER)


                square.grid(row = r, column = c, sticky = E)
                self.squares[r][c] = square

                text_color = "white" if bonus in ("L3", "W3") else "black"



        



def main():
    win = tk.Tk()
    display = Display(win)
    win.mainloop()


# def main():
#   window = tk.Tk()
#   window.mainloop()
    

#   window.geometry('1000x1000')
#   btn = Button(window, text = "Start Game", command = start_game)



if __name__ == '__main__':
    main()