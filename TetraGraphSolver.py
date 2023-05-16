from collections import namedtuple
import copy

#ADDING LAST_VISTED TO NODE DEF SO WE CAN PROPERLY RE_ROTATE TO NEXT POSITION FROM PREVIOUS (INSTEAD OF LOOPING FROM CURRENT)
direction_matrix = [-1, 1, 1, -1]
level = [[2, 1, 1], [1, 1, 2], [1, 1, 2]]
row_width = 3
col_height = 3
#current_path = []
all_paths = [[]]
num_poly_sides = 4


class Node:

    def __init__(self, value, r, c):
        self.last_visited = None
        self.value = value
        self.visited = False
        self.targets = []
        Location = namedtuple('Location', ['row', 'col'])
        self.location = Location(r, c)
        self.direction = 0
        self.all_paths_found_from_here = False

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
        for r in range(col_height):
            for c in range(row_width):
                for i in range(
                        num_poly_sides
                ):  #number of sides of polygon (square in this case, hexagon in hexbon/bee game)
                    if (i % 2) == 0:
                        self.target_row = r + self.board[r][
                            c].value * direction_matrix[i]
                        self.target_col = c
                    else:
                        self.target_row = r
                        self.target_col = c + self.board[r][
                            c].value * direction_matrix[i]
                    if ((self.target_row < 0)
                            or (self.target_row >= col_height)
                            or (self.target_col < 0)
                            or (self.target_col >= row_width)):
                        self.board[r][c].targets.append(None)
                    else:
                        self.board[r][c].targets.append(
                            self.board[self.target_row][self.target_col])

    def display(self):
        for row in self.board:
            print(*row)

    def show_targets(self):
        for r, row in enumerate(self.board):
            for c, node in enumerate(row):
                for i in range(num_poly_sides):
                    if self.board[r][c].targets[i] is not None:
                        print(
                            "Node [{}][{}] -> Target {} : [{}][{}],Value -> {}"
                            .format(r, c, i,
                                    self.board[r][c].targets[i].location.row,
                                    self.board[r][c].targets[i].location.col,
                                    self.board[r][c].targets[i].value))
                    else:
                        print("NONE")
        print()


class Walker:
    start_node = None
    current_node = None
    prev_node = None
    current_path = []
    direction = 0

    def __init__(self, board, row, col):
        '''we do this separate from "current_node" so we know when we backtrack to this, we can backtrack no more'''
        self.start_node = board[row][col]
        self.start_node.visited = True
        self.current_node = self.start_node
        self.prev_node = self.start_node
        self.current_node.visited = True
        self.current_path.append(self.start_node)

    def scan(self):
        print(f"Scanning:[{self.current_node.location.row}][{self.current_node.direction}]: {self.current_node.direction}")

        if (self.current_node.direction >= num_poly_sides):
            all_paths.append(copy.deepcopy(self.current_path))
            #for p in a:
            #    print(f"Printing all Paths: [{p.location.row}][{p.location.col}]")
            self.backtrack()
            self.turn_right()
        elif (
                self.current_node.targets[self.current_node.direction] is None
        ) or (self.current_node.targets[self.current_node.direction].visited):
            print("Target null/visited")
            self.turn_right()
            print("Node[{}][{}] Direction -> {}".format(
                self.current_node.location.row, self.current_node.location.col,
                self.current_node.direction))
            print()
            self.scan()
        else:
            print("Valid Target. Moving...")
            self.move()
            print("Moved to Node[{}][{}]".format(
                self.current_node.location.row,
                self.current_node.location.col))
            print("PATH SO FAR:")
            for s in self.current_path:
                print("[{}],[{}] ".format(s.location.row, s.location.col))
            self.scan()


#THIS RIGHT HERE

    def turn_right(self):
        print("Turning Right...")
        self.current_node.set_direction(self.current_node.direction + 1)

    def move(self):
        self.current_node.last_visited = self.current_node.targets[
            self.current_node.direction]
        self.current_node = self.current_node.targets[
            self.current_node.direction]
        self.current_node.visited = True
        self.current_path.append(copy.deepcopy(self.current_node))

    def backtrack(self):
        print(
            f"Backtracking to [{self.prev_node.location.row}][{self.prev_node.location.row}]"
        )
        self.current_node = self.prev_node
        if self.current_node == self.start_node:  # AND direction = 4
            self.current_node.all_paths_found_from_here = True
            print("all paths found")
            return
        else:
            self.scan()
            return

    def walk(self):
        self.scan()
        self.move()
        self.walk()

b = Board(level)
b.display()
b.show_targets()
w = Walker(b.board, 0, 0)
w.walk()
