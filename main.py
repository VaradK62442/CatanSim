import random
import tkinter as tk
from math import sqrt
import matplotlib.pyplot as plt


# generating the board

# rules for generation:
#   randomly place terrain tiles
#   allocate tokens in order from top left moving anti-clockwise in a spiral
#   (skipping over dessert)

# terrain tiles
#   dessert - 1
#   wheat - 4
#   sheep - 4
#   wood - 4
#   brick - 3
#   ore - 3

# roll tokens (in anti-clockwise order)
#   5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11

# roll tokens (in left to right order)
#   5, 10, 8, 
#   2, 9, 11, 4,
#   6, 4, d, 3, 11, 
#   3, 5, 6, 12, 
#   8, 10, 9


# create a class for tiles

class Tile:
    def __init__(self, type, token):
        self.type = type
        self.token = token


# display board with tkinter

def display_results(board, count, rolls):

    # function to draw hexagon with given radius, and (x, y) offset
    def draw_hex(r, off_x, off_y):
        colours = {
            'dessert': '#ffea00',
            'wheat': '#fc9642',
            'sheep': '#c1fc42',
            'wood': '#55fc42',
            'brick': '#fc4258',
            'ore': '#7a7a7a'
        }

        # points starts at top and continue clockwise
        points = [
            0 + off_x, r + off_y,                       # top
            sqrt(3)*r/2 + off_x, r/2 + off_y,           # top right
            sqrt(3)*r/2 + off_x, (-1)*r/2 + off_y,      # bottom right
            0 + off_x, (-1)*r + off_y,                  # bottom
            (-1)*sqrt(3)*r/2 + off_x, (-1)*r/2 + off_y, # bottom left
            (-1)*sqrt(3)*r/2 + off_x, r/2 + off_y       # top left
        ]
    
        canvas.create_polygon(points, outline="black", fill = colours[tile.type], width=2)


    root = tk.Tk()
    root.title("Catan")

    board_frame = tk.Frame(root)
    board_frame.pack()

    # radius of hexagon
    r = 50

    canvas = tk.Canvas(board_frame, width=f"{16*r}", height=f"{16*r}")
    canvas.grid()

    base_xs = [6*r, 5*r, 4*r, 5*r, 6*r]
    base_y = 2.3*r # 4*r - 1.7*r

    for i, row in enumerate(board):
        base_x = base_xs[i]
        base_y = base_y + 1.7*r

        for i, tile in enumerate(row):
            # offset
            off_x = base_x + i * r * 2
            off_y = base_y

            draw_hex(r, off_x, off_y)

            canvas.create_text(off_x, off_y, text=f"{tile.type} - {tile.token}", fill="black")


    # display results
    
    count = {k: v for k, v in sorted(count.items(), key=lambda item: item[1])}

    plt.figure(1)
    plt.bar([k for k in count], [count[k] for k in count])
    plt.ylabel("Number of times resources was generated")
    plt.xlabel("Resource name")
    plt.title("Count of resources generated over multiple rolls")

    # rolls = {k: v for k, v in sorted(rolls.items(), key=lambda item: item[1])}

    plt.figure(2)
    plt.bar([k for k in rolls], [rolls[k] for k in rolls])
    plt.ylabel("Number of times a number was rolled")
    plt.xlabel("Number rolled")
    plt.title("Frequency of rolls")

    plt.show()
    root.mainloop()


# randomly generate board

def gen_board():
    # generate a standard board
    # rows of 3, 4, 5, 4, 3 tiles
    board = []
    tiles = ['dessert'] + ["wheat"]*4 + ['sheep']*4 + ['wood']*4 + ['brick']*3 + ['ore']*3
    
    # allocate tile types
    for i in range(5):
        board.append([])
        if i == 0 or i == 4:
            for _ in range(3):
                tile_choice = random.choice(tiles)
                tile = Tile(tile_choice, 7)
                board[i].append(tile)
                tiles.remove(tile_choice)
        elif i == 1 or i == 3:
            for _ in range(4):
                tile_choice = random.choice(tiles)
                tile = Tile(tile_choice, 7)
                board[i].append(tile)
                tiles.remove(tile_choice)
        else:
            for _ in range(5):
                tile_choice = random.choice(tiles)
                tile = Tile(tile_choice, 7)
                board[i].append(tile)
                tiles.remove(tile_choice)

    # allocate token
    tokens = [5, 10, 8, 2, 9, 11, 4,6, 4, 3, 11, 3, 5, 6, 12, 8, 10, 9]

    for row in board:
        for tile in row:
            if tile.type != "dessert":
                tile.token = tokens[0]
                tokens = tokens[1:]

    return board


# simulate dice rolls and keep track of which resources are rolled
 
def simulate(board, reps):
    count = {
        'dessert': 0,
        'wheat': 0,
        'sheep': 0,
        'wood': 0,
        'brick': 0,
        'ore': 0
    }

    #  to count frequency of rolls
    roll_freq = {
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0
    }

    for _ in range(reps):
        # generate roll
        roll = random.randint(1, 6) + random.randint(1, 6)

        roll_freq[roll] += 1

        # check which resources were generated
        for row in board:
            for tile in row:
                if tile.token == roll:
                    count[tile.type] += 1


    return count, roll_freq


# main

def main():
    reps = 1_000_000
    board = gen_board()
    count, rolls = simulate(board, reps)
    display_results(board, count, rolls)


if __name__ == "__main__":
    main()