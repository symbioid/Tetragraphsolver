from collections import namedtuple
import copy
import os
direction_matrix = [-1, 1, 1, -1]
level = [[2, 1, 1], [1, 1, 2], [1, 1, 2]]
ROW_WIDTH = 3
COL_HEIGHT = 3
NUM_POLY_SIDES = 4
all_paths = [[]]
class Node:
    '''A class to represent a node in a grid.

    Attributes: last_visited (Node): The previous node visited by the search algorithm. value (int): The value of the node. visited (bool): A flag to indicate whether the node has been visited or not. targets (list of Node): A list of nodes that are reachable from this node. location (namedtuple): A namedtuple with row and col attributes to store the coordinates of the node. direction (int): An integer to indicate the direction of the search algorithm (0: right, 1: down, 2: left, 3: up). all_paths_found_from_here (bool): A flag to indicate whether all possible paths from this node have been explored or not.

    Methods: init(self, value, row, col): Initializes a Node object with the given value and location. repr(self): Returns a string representation of the node value. get_direction(self): Returns the direction attribute of the node. set_direction(self, value): Sets the direction attribute of the node to the given value. '''
    def __init__(self, value, row, col):
        self.last_visited = None
        self.value = value
        self.visited = False
        self.targets = []
        Location = namedtuple('Location', ['row', 'col'])
        self.location = Location(row, col)
        self.direction = 0
        self.all_paths_found_from_here = False
    def __repr__(self):
        return str(self.value)
    def get_direction(self):
        return self.direction
    def set_direction(self, value):
        self.direction = value
class Board:
    ''' A class to represent a board of nodes in a grid.

    Attributes: board (list of list of Node): A two-dimensional list of Node objects that form the grid. target_row (int): The row index of the target node for the current node. target_col (int): The column index of the target node for the current node.

    Methods: init(self, width): Initializes a Board object with the given width, which is a list of lists of integers representing the values of the nodes. It also creates the Node objects and assigns them their targets based on the direction_matrix and the board dimensions. display(self): Prints the board to the standard output, showing the values of each node. show_targets(self): Prints the targets of each node to the standard output, showing their coordinates and values. If a target is None, it means that it is out of bounds. '''
    board = []
    target_row = 0
    target_col = 0
    def __init__(self, width):
        for r, row in enumerate(width):
            board_row = []
            for c, value in enumerate(row):
                board_row.append(Node(value, r, c))
            self.board.append(board_row)
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
    '''A class to represent a walker that traverses the board of nodes in a grid.

    Attributes: start_node (Node): The node where the walker starts its journey. current_node (Node): The node where the walker is currently located. prev_node (Node): The node where the walker was previously located. current_path (list of Node): A list of nodes that form the current path of the walker. direction (int): An integer to indicate the direction of the walker (0: right, 1: down, 2: left, 3: up).

    Methods: init(self, board, row, col): Initializes a Walker object with the given board, which is a two-dimensional list of Node objects, and the row and col indices of the start node. It also marks the start node as visited and adds it to the current path. scan(self): Scans the target node of the current node based on its direction. If the target node is None or visited, it turns right and scans again. If the target node is valid, it moves to it and scans again. If the current node has exhausted all its directions, it appends the current path to the global list of paths and backtracks to the previous node. turn_right(self): Turns the walker right by incrementing its direction attribute by one. move(self): Moves the walker to its target node based on its direction attribute. It also updates the prev_node, current_node, and current_path attributes accordingly. backtrack(self): Moves the walker back to its previous node. It also pops the last node from the current path and scans again. If the current node is the start node, it sets its all_paths_found_from_here attribute to True and prints all the paths found from it. walk(self): Starts the walking process by calling scan and move recursively until all paths are found or exhausted. '''
    start_node = None
    current_node = None
    prev_node = None
    current_path = []
    direction = 0
    def __init__(self, board, row, col):
        self.start_node = board[row][col]
        self.start_node.visited = True
        self.current_node = self.start_node
        self.prev_node = None
        self.current_node.visited = True
        self.current_path.append(self.start_node)
    def scan(self):
        if (self.current_node.direction >= NUM_POLY_SIDES):
            print("End of Path, Appending to list of Paths")
            all_paths.append(self.current_path)
            #for idx, p in enumerate(all_paths):
            #    for n in p:
            #        print(f"Printing Path[{idx}]: [{n.location.row}][{n.location.col}]")
            #    print("\n")
            self.backtrack()
            if self.current_node.all_paths_found_from_here:
                exit()
            self.turn_right()
        elif (
                self.current_node.targets[self.current_node.direction] is None
        ) or (self.current_node.targets[self.current_node.direction].visited):
            print("Target null/visited\n")
            self.turn_right()
            self.scan()
        else:
            print("Valid Target. Moving...")
            self.move()
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
        self.current_node = self.current_node.targets[self.current_node.direction]
        self.current_node.visited = True
        self.current_path.append(copy.deepcopy(self.current_node))
    def backtrack(self):
        self.current_node = self.prev_node
        print('\n')
        if self.current_node != self.start_node:
            a = self.current_path.pop()
            print(f"POPPING: : [{a.location.row}], [{a.location.col}]")
            print("After Backtrack - Path is : ")
            for idx, n in enumerate(self.current_path):
                print(f"{idx}: [{n.location.row},{n.location.col}]")
        if len(self.current_path) == 0:
            self.current_node.all_paths_found_from_here = True
            print(f"all paths found from [{self.start_node.location.row}][{self.start_node.location.col}]")
            for idx, p in enumerate(all_paths):
                for n in p:
                    print(f"Printing Path[{idx}]: [{n.location.row}][{n.location.col}]")
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
