import tkinter as tk
from tkinter import N, S, E, W, NE, NE, SE, SW
from Scrabble import Scrabble

tile_size = 40
tile_center = (tile_size//2, tile_size//2)
board_size = 15 * tile_size

mini_square = [(0,0),(0,1),(1,1),(1,0)]

leftclick = '<Button-1>'

class Display():
    def __init__(self, win, game = None):
        self.game = game or Scrabble()
        self.win = win
        self.win.geometry('1000x900+2000+50')
        self.board = DisplayBoard(master = self.win, game = self.game)
        self.board.grid(padx=5, pady=5, rowspan = 15, columnspan = 15)

        self.rack = DisplayRack(master = self.win, game = self.game)
        self.rack.grid(padx=5, pady = 5, row = 16, columnspan = 7)


        closebutton = tk.Button(self.win, text="close", width=10, command=self.win.destroy)
        closebutton.grid(column = 0, sticky = SW)
        self.board.create_board()


    def place_tile(tile, location):
        """ Move a tile to a given location"""
        pass

class DisplayRack(tk.Frame):
    def __init__(self, master, game):
        self.master = master
        self.game = game

        super().__init__(self.master, width = tile_size * 7, height = tile_size)

    def handle_tile_click():
        pass

    def refill_rack(self):
        for ind, tile in enumerate(self.game.current_player.rack):
            pass



class DisplayBoard(tk.Frame):
    def __init__(self, master, game):
        self.game = game or Scrabble()
        self.game_board = self.game.board
        self.master = master

        super().__init__(self.master, width = board_size, height = board_size)
        
        self.squares = [[None] * 15 for _ in range(15)]
        self.current_move = []
        self.focus_tile = []

    

    def swap_tiles_at(loc_1, loc_2):
        r1,c1 = loc_1
        r2,c2 = loc_2
        self.squares[r1][c1].grid(loc_2)
        self.squares[r2][c2].grid(loc_1)

    def handle_click(self, r, c):
        """ Handle click on the square at (r, c)"""
        if self.game_board[r,c].occupied:
            return

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
                bg_color = bonus_color_lookup.get(bonus, 'beige')
                text_color = "white" if bg_color in ("Blue", "Red") else "black"

                square = tk.Canvas(self, width = tile_size, height = tile_size, bg = bg_color, 
                    borderwidth = 1, relief = tk.RIDGE, 
                    highlightcolor = 'black', highlightbackground = 'black')

                func = get_click_function(r, c)

                square.bind(leftclick, func)

                bonus_text = bonus_text_lookup.get(bonus, None)
                if bonus_text:
                    text = square.create_text(tile_center, text = bonus_text, font = ("Arial", 10), fill = text_color, justify = tk.CENTER)


                square.grid(row = r, column = c)
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