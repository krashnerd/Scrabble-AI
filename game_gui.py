import tkinter as tk
from Scrabble import Scrabble

tile_size = 40

mini_square = [(0,0),(0,1),(1,1),(1,0)]

def show_board():
    import tkinter as tk

    game = Scrabble()
    board = game.board
    top = tk.Tk()
    w = tk.Canvas(top, bg = 'white', width = tile_size * 15, height = tile_size * 15)
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

            coords = [((r + a) * tile_size, (c + b) * tile_size) for a,b in mini_square]
            x, y = ((r + .5) * tile_size, (c + .5) * tile_size)


            square = w.create_polygon(coords, outline = "black", fill = bonusGuide.get(board[r,c].bonusType,'tan'))

            w.create_text(x, y, font="Purisa", text=str((r, c)))



    w.pack()
    top.mainloop()

def main():
    show_board()

# def main():
#   window = tk.Tk()
#   window.mainloop()
    

#   window.geometry('1000x1000')
#   btn = Button(window, text = "Start Game", command = start_game)



if __name__ == '__main__':
    main()