import tkinter as tk
from tkinter import N, S, E, W, NE, NW, SE, SW
import Scrabble

tile_size = 40
tile_center = (tile_size//2, tile_size//2)
board_size = 15 * tile_size

mini_square = [(0,0),(0,1),(1,1),(1,0)]

leftclick = '<Button-1>'

class Display():
    def __init__(self, win, game = None):
        self.game = game or Scrabble.Scrabble()
        game = self.game
        self.win = win
        self.win.geometry('1000x900+2000+50')
        self.tiles = {}
        self.rack = DisplayRack(self, self.game)

        self.board = DisplayBoard(self, self.game)
        self.board.create_board()
        self.tiles.update({tile: DisplayTile(self, tile) for tile in game.bag.all_tiles})

        

        # self.board.grid(padx=5, pady=5, rowspan = 15, columnspan = 15, sticky = NW)


        

        self.rack.refill_rack()

        closebutton = tk.Button(self.win, text="close", width=10, command=self.win.destroy)
        closebutton.grid(column = 0, rowspan = 2, sticky = S + W)
        self.win.bind('q', self.destroy)
        print("Size:", self.win.grid_size())



    def destroy(self, event):
        self.win.destroy()
        
    def place_tile(tile, location):
        """ Move a tile to a given location"""
        pass

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

        self.letter = game_tile.letter
        self.points = game_tile.points

        super().__init__(self.win, width = tile_size, height = tile_size)

        self.create_rectangle(0,0,tile_size,tile_size, fill = 'beige')
        self.create_text(tile_center, text = self.letter, font = ("Arial", 24))
        self.create_text((35, 35), text = str(self.points), font = ("Arial", 8))

        self.bind(leftclick, self.handle_click)

    def handle_click(self, event):
        self.focus_set()

    def __eq__(self, other):
        return ((isinstance(other, DisplayTile) and self.game_tile == other.game_tile) or
            (isinstance(other, Scrabble.Tile) and self.game_tile == other))

class DisplayBoard(tk.Frame):
    def __init__(self, display, game):
        self.display = display
        self.master = self.display.win
        self.game = game or Scrabble.Scrabble()
        self.game_board = self.game.board

        super().__init__(self.master, width = board_size, height = board_size)
        
        self.squares = [[None] * 15 for _ in range(15)]
        self.current_move = dict()
        self.focus_tile = []

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


    def take_rack_tile(self, display_tile):
        new_tile = DisplayTile(self.d)



    def handle_click(self, r, c):
        """ Handle click on the square at (r, c)"""
        if self.game_board[r,c].occupied:
            return

        focused = self.master.focus_get()
        if isinstance(focused, DisplayTile):
            # self.squares[r][c].grid_forget()
            focused.grid(row = r, column = c, pady = 0)

        return


        self.swap_tiles_at((0,0),(0,1))
        print("Clicked on {}".format((r,c)))



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