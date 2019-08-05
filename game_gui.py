import tkinter as tk
from Scrabble import Scrabble

tile_size = 40
board_size = 15 * tile_size

mini_square = [(0,0),(0,1),(1,1),(1,0)]


class Display():
    def __init__(self, win):
        self.win = win
        # self.board = tk.Frame(width = board_size, height = board_size, bg = 'Beige')

        self.canvas = tk.Canvas(self.win, bg = 'white', width = tile_size * 15 + 300, height = tile_size * 15 + 150)

    def test_pack(self):
        self.canvas.create_text(100, 100, font=("Arial", 16), text = "poop", fill = "black")
        
        self.canvas.pack()

    def show_board(self):
        game = Scrabble()
        board = game.board
        w = self.canvas
        bonusColor = {
                    None:'Beige',
                    'L2':'Cyan',
                    'W2':'Pink',
                    'L3':'Blue',
                    'W3':'Red',
                    }
        bonusText = {
                    None:'',
                    'L2':'DLS',
                    'W2':'DWS',
                    'L3':'TLS',
                    'W3':'TWS',
                    }


        for c in range(15):
            for r in range(15):
                tile = board[r,c]
                coords = [((r + a) * tile_size, (c + b) * tile_size) for a,b in mini_square]
                x, y = ((r + .5) * tile_size, (c + .5) * tile_size)

                bonus = tile.bonusType

                square = w.create_polygon(coords, outline = "black", fill = bonusColor.get(bonus,'tan'))

                text_color = "white" if bonus in ("L3", "W3") else "black"
                w.create_text(x, y, font=("Arial", 16), text = bonusText.get(bonus, ''), fill = text_color)

        closebutton = tk.Button(w, text="get", width=10, command=self.test_pack)
        closebutton.place(x = 650, y = 650)
        w.pack()




def main():
    win = tk.Tk()
    display = Display(win)
    display.show_board()
    win.mainloop()


# def main():
#   window = tk.Tk()
#   window.mainloop()
    

#   window.geometry('1000x1000')
#   btn = Button(window, text = "Start Game", command = start_game)



if __name__ == '__main__':
    main()