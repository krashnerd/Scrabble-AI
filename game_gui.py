import tkinter as tk
from tkinter import N, S, E, W, NE, NE, SE, SW
from Scrabble import Scrabble

tile_size = 40
tile_center = (tile_size//2, tile_size//2)
board_size = 15 * tile_size

mini_square = [(0,0),(0,1),(1,1),(1,0)]


class Display():
    def __init__(self, win, game = None):
        self.game = game or Scrabble()
        self.win = win
        self.win.geometry('1000x900+2000+50')
        self.board = tk.Frame(self.win, width = board_size, height = board_size)
        self.board.grid(padx=5, pady=5, rowspan = 15, columnspan = 15)
        self.board_squares = [[None] * 15 for _ in range(15)]


    def full_text(bonus_code):

        b_type, b_number = list(bonus_code)

    def create_board(self):
        board = self.game.board
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

        for c in range(15):
            for r in range(15):
                tile = board[r,c]
                coords = [((r + a) * tile_size, (c + b) * tile_size) for a,b in mini_square]
                x, y = ((r + .5) * tile_size, (c + .5) * tile_size)

                bonus = tile.bonusType
                bg_color = bonus_color_lookup.get(bonus, 'beige')
                text_color = "white" if bg_color in ("Blue", "Red") else "black"
                square = tk.Canvas(self.board, width = tile_size, height = tile_size, bg = bg_color, 
                    borderwidth = 1, relief = tk.RIDGE, 
                    highlightcolor = 'black', highlightbackground = 'black')
                bonus_text = bonus_text_lookup.get(bonus, None)
                if bonus_text:
                    text = square.create_text(tile_center, text = bonus_text, font = ("Arial", 10), fill = text_color)


                square.grid(row = r, column = c)
                self.board_squares[r][c] = square

                text_color = "white" if bonus in ("L3", "W3") else "black"

        closebutton = tk.Button(self.win, text="close", width=10, command=self.test_pack)
        closebutton.grid(column = 0, sticky = SW)



def main():
    win = tk.Tk()
    display = Display(win)
    display.create_board()
    win.mainloop()


# def main():
#   window = tk.Tk()
#   window.mainloop()
    

#   window.geometry('1000x1000')
#   btn = Button(window, text = "Start Game", command = start_game)



if __name__ == '__main__':
    main()