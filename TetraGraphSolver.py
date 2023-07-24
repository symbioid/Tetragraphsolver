from collections import namedtuple
import copy

#ADDING LAST_VISTED TO NODE DEF SO WE CAN PROPERLY RE_ROTATE TO NEXT POSITION FROM PREVIOUS (INSTEAD OF LOOPING FROM CURRENT)
direction_matrix = [-1, 1, 1, -1]
level = [[2, 1, 1], [1, 1, 2], [1, 1, 2]]
ROW_WIDTH = 3
COL_HEIGHT = 3
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
    def __init__(self, width):
        for r, row in enumerate(width):
            board_row = []
            for c, value in enumerate(row):
                board_row.append(Node(value, r, c))
            self.board.append(board_row)


    # Add Targets to each Node
        for r in range(COL_HEIGHT):
            for c in range(ROW_WIDTH):
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
                            or (self.target_row >= COL_HEIGHT)
                            or (self.target_col < 0)
                            or (self.target_col >= ROW_WIDTH)):
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
                        node = self.board[r][c]
                        print(f"Node [{r}][{c}] -> Target {i} : [{node.targets[i].location.row}][{node.targets[i].location.col}],Value -> {node.targets[i].value}")
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
        self.prev_node = None
        self.current_node.visited = True
        self.current_path.append(self.start_node)

    def scan(self):
        print(f"Scanning:[{self.current_node.location.row}][{self.current_node.location.col}]: {self.current_node.direction}")

        if (self.current_node.direction >= num_poly_sides):
            print("End of Path, Appending to list of Paths")
            all_paths.append(copy.deepcopy(self.current_path))
            for idx, p in enumerate(all_paths):
                for n in p:
                    print(f"Printing Path[{idx}]: [{n.location.row}][{n.location.col}]")
            print("\n")
            self.backtrack()
            if self.current_node.all_paths_found_from_here:
                exit()
            self.turn_right()
        elif (
                self.current_node.targets[self.current_node.direction] is None
        ) or (self.current_node.targets[self.current_node.direction].visited):
            print("Target null/visited")
            self.turn_right()
            print(f"Node[{self.current_node.location.row}][{self.current_node.location.col}] Direction -> {self.current_node.direction}")
            print()
            self.scan()
        else:
            print("Valid Target. Moving...")
            self.move()
            print("Moved to Node[{}][{}]".format(
                self.current_node.location.row,
                self.current_node.location.col))
            print("PATH SO FAR:")
            for node in self.current_path:
                print(f"[{node.location.row}],[{node.location.col}] ")
            self.scan()


    def turn_right(self):
        print(f"Turning RIGHT! [{self.current_node.direction}] -> [{self.current_node.direction + 1}]")
        self.current_node.set_direction(self.current_node.direction + 1)


    def move(self):
        self.prev_node = self.current_node
        if self.current_node is not self.start_node:
            self.current_node.last_visited = self.current_node.targets[
                self.current_node.direction]
        self.current_node = self.current_node.targets[
            self.current_node.direction]
        self.current_node.visited = True
        self.current_path.append(copy.deepcopy(self.current_node))


#PREVNODE stuck at [2,2]
    def backtrack(self):
        print(f"Current Node is Now : [{self.current_node.location.row}][{self.current_node.location.col}]")
        self.current_node = self.prev_node
        self.current_node.visited = False
        if self.current_node != self.start_node :
            print(f"Backtracking to [{self.prev_node.location.row}][{self.prev_node.location.col}]")

            print(f"Current Node is Now : [{self.current_node.location.row}][{self.current_node.location.col}]")
            a = self.current_path.pop()

            print(f"this is node popped: {a.location.row}, {a.location.col}")
            print("After Popping, Path is: ")
            for idx, n in enumerate(self.current_path):
                print(f"{idx}: [{n.location.row},{n.location.col}]")

        if len(self.current_path) == 0:  # AND direction = 4
            self.current_node.all_paths_found_from_here = True
            print(f"all paths found from [{self.start_node.location.row}][{self.start_node.location.col}]")
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
