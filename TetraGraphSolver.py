from collections import namedtuple
import copy


direction_matrix = [-1, 1, 1, -1]
level = [[2, 1, 1], [1, 1, 2], [1, 1, 2]]
board_size = 3
#current_path = []
all_paths = [[]]
num_poly_sides = 4


class Node:
    def __init__(self, value, r, c):
        self.value = value
        self.visited = False
        self.targets = []
        Location = namedtuple('Location', ['row', 'col'])
        self.location = Location(r, c)
        self.direction = 0

    def __repr__(self):
        return str(self.value)
    def get_direction(self):
        return self.direction
    def set_direction(self, value):
        self.direction = value

class Board:
    board = []
    target_row = 0
    target_col = 0

    # Make Board
    def __init__(self, l):
        for r, row in enumerate(l):
            board_row = []
            for c, value in enumerate(row):
                board_row.append(Node(value, r, c))
            self.board.append(board_row)

		# Add Targets to each Node
        for r in range(board_size):
            for c in range(board_size):
                for i in range(num_poly_sides):  #number of sides of polygon (square in this case, hexagon in hexbon/bee game)
                    if (i % 2) == 0:
                        self.target_row = r + self.board[r][c].value * direction_matrix[i]
                        self.target_col = c
                    else:
                        self.target_row = r
                        self.target_col = c + self.board[r][c].value * direction_matrix[i]
                    if((self.target_row < 0) or (self.target_row >= board_size) or (self.target_col < 0) or (self.target_col >= board_size)):
                        self.board[r][c].targets.append(None)
                    else:
                        self.board[r][c].targets.append(self.board[self.target_row][self.target_col])
    def display(self):
        for row in self.board:
            print(*row)

    def show_targets(self):
        for r, row in enumerate(self.board):
            for c, node in enumerate(row):
                for i in range(num_poly_sides):
                    if self.board[r][c].targets[i] is not None:
                        print("Node [{}][{}] -> Target {}: [{}][{}],Value -> {}".format(r, c, i, self.board[r][c].targets[i].location.row, self.board[r][c].targets[i].location.col, self.board[r][c].targets[i].value))
                    else:
                        print("Node [{}][{}] -> Target {}: [-][-],Value -> NULL".format(r, c, i))
                print("----------------------------------------------")
        print()



b = Board(level)
b.display()
b.show_targets()
