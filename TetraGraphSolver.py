from collections import namedtuple
import copy
import os

direction_matrix = [-1, 1, 1, -1]
adjacent_direction_inversion = [2, 3, 0, 1]
# targetnode.visited_by_direction[adjacent_direction_inversion[current_node.direction]] = True then move
level = [[2, 1, 1], [1, 1, 2], [1, 1, 2]]
ROW_WIDTH = 3
COL_HEIGHT = 3
NUM_POLY_SIDES = 4
all_paths = [[]]

# class Node:
#     def __init__(self, value, row, col):
#         #self.last_visited = None
#         self.value = value
#         self.visited = False
#         self.targets = []
#         Location = namedtuple('Location', ['row', 'col'])
#         self.location = Location(row, col)
#         self.direction = 0
#         self.all_paths_found_from_here = False
#         self.visited_by_direction = [False, False, False, False]


class Node:
    def __init__(self, value, row, col):
        self.value = value
        self.targets = []
        Location = namedtuple('Location', ['row', 'col'])
        self.location = Location(row, col)
        self.id = str(row) + str(col)
        self.last_visited_direction = 0
        #when building nodes - scan each outward node, add that as the "target node" for that direction on this node, and also mark that target's "visited by node" as this node - self.name = str(row){col}" for key and bool as visited value
        self.visited_by_node = {}

row = 0
col = 0
n = Node(2,2,4)


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
                for i in range(NUM_POLY_SIDES):
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
                for i in range(NUM_POLY_SIDES):
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
        self.start_node = board[row][col]
        self.prev_node = None
        self.start_node.visited = True
        self.current_node = self.start_node
        self.current_node.visited = True
        self.current_path.append(self.start_node)

    def scan(self):
        print(f"Scanning:[{self.current_node.location.row}][{self.current_node.location.col}]: {self.current_node.direction}")

        if (self.current_node.direction == NUM_POLY_SIDES):
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

        elif (self.current_node.targets[self.current_node.direction] is None) or (self.current_node.targets[self.current_node.direction].visited_by_direction[adjacent_direction_inversion[self.current_node.direction]]) or (self.current_node.targets[self.current_node.direction] == self.start_node) or(self.current_node.targets[self.current_node.direction].visited) :
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
        self.current_node.visited_by_direction[adjacent_direction_inversion[self.prev_node.direction]] = True
        self.current_node.visited = True
        self.current_path.append(copy.deepcopy(self.current_node))


    def backtrack(self):
        print(f"Current Node is Now : [{self.current_node.location.row}][{self.current_node.location.col}]")
        if self.current_node != self.start_node :
            print("Backtracking...")
            self.current_node = self.prev_node
            a = self.current_path.pop()
            print(f"POPPING: : [{a.location.row}][{a.location.col}]")
            print(f"Current Node is Now : [{self.current_node.location.row}][{self.current_node.location.col}]")
            print(f"[{a.location.row}][{a.location.col}].visited :  {a.visited}")
            print("After Popping, Path is: ")
            for idx, n in enumerate(self.current_path):
                print(f"{idx}: [{n.location.row},{n.location.col}]")

        if not self.current_path :
            self.current_node.all_paths_found_from_here = True
            print(f"all paths found from [{self.start_node.location.row}][{self.start_node.location.col}]")
            #for idx, p in enumerate(all_paths):
            #    for n in p:
            #        print(f"Printing Path[{idx}]: [{n.location.row}][{n.location.col}]")
            #    print("\n")
            return
        self.scan()
        return

    def walk(self):
        self.scan()
        self.move()
        self.walk()

os.system('clear')
b = Board(level)
b.display()
b.show_targets()
w = Walker(b.board, 0, 0)
w.walk()
