from collections import namedtuple
import copy

direction_matrix = [-1, 1, 1, -1]
level = [[2, 1, 1], [1, 1, 2], [1, 1, 2]]
board_size = 3
current_path = []
all_paths = []
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
                        print(f"Node [{r}][{c}] -> Target {i} : [{self.board[r][c].targets[i].location.row}][{self.board[r][c].targets[i].location.col}] = {self.board[r][c].targets[i].value}")
                    else:
                        print(f"Node [{r}][{c}] -> Target {i} : [NONE] = -")
        print()

class Walker:
    start_node = None
    current_node = None
    prev_node = None
    current_path = []

    def __init__(self, board, row, col):
        self.start_node = board[row][col] #we do this separate from "current_node" so we know when we backtrack to this, we can backtrack no more
        self.start_node.visited = True
        self.current_node = self.start_node
        self.prev_node = self.start_node
        self.current_path.append(self.current_node)




    def scan(self):
        print("Scanning:")
        if (self.current_node.direction >= num_poly_sides):
            all_paths.append(self.current_path)
            for a in all_paths:
                for p in a:
                    print(f"Printing all Paths: [{p.location.row}][{p.location.col}]")
            print("Backtracking...")
            self.backtrack()
            self.turn_right()
        elif ((self.current_node.targets[self.current_node.direction] is None) or (self.current_node.targets[self.current_node.direction].visited is True)): #THIS HERE
            print(f"Node[{self.current_node.location.row}][{self.current_node.location.col}] Direction -> {self.current_node.direction}")
            print("Target null/visited")
            self.turn_right()
            print(f"Node[{self.current_node.location.row}][{self.current_node.location.col}] Direction -> {self.current_node.direction}")
            print()
            self.scan()
        else:
            self.move()
            self.scan()

    def turn_right(self):
        print(f"current direction {self.current_node.direction}")
        print("Turning Right...")
        self.current_node.set_direction(self.current_node.direction + 1)
        print(f"current direction {self.current_node.direction}")

    def move(self): #vs here?  what?  JFC.
        print("Valid Target. Preparing to Jump...")
        self.current_node.visited = True
        self.current_node = self.current_node.targets[self.current_node.direction]
        self.current_path.append(self.current_node)

        #if self.current_node != self.start_node:
        print("PATH SO FAR:")
        for s in self.current_path:
            print(f"[{s.location.row}],[{s.location.col}]")
            self.prev_node = self.current_node
            print(f"CURRENT PATH: {self.current_path}")


    def backtrack(self):  #Backtrack needs to happen on failure, not just success.
        print("backtracking")
        self.current_node.visited = False
        self.current_node = self.prev_node

        if self.current_node == self.start_node: # AND direction = 4
            print("all paths found")
            return
        else:
            self.scan()
            return

    def walk(self):
        self.scan()
        #self.move()
        #self.walk()



b = Board(level)
b.display()
b.show_targets()
w = Walker(b.board, 0, 0)
w.walk()

