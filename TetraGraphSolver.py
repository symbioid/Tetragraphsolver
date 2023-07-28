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
    '''This class represents a node in a graph.

    Attributes:
    - last_visited: A reference to the last visited node from this node. (Default: None)
    - value: The value of the node.
    - visited: A boolean indicating if the node has been visited or not. (Default: False)
    - targets: A list of nodes that can be reached from this node.
    - location: A namedtuple representing the location of the node in the graph, with 'row' and 'col' attributes.
    - direction: The direction of the node. (Default: 0)
    - all_paths_found_from_here: A boolean indicating if all paths from this node have been found. (Default: False)

    Methods:
    - __repr__: Returns a string representation of the node.
    - get_direction: Returns the direction of the node.
    - set_direction: Sets the direction of the node.'''

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
    """
    This class represents a game board.
    Attributes:

    size: The size of the board (number of rows and columns).
    graph: A dictionary representing the graph structure of the board, where the keys are the nodes and the values are the corresponding node objects.
    obstacles: A list of nodes that represent obstacles on the board.
    start: The starting node of the board.
    end: The ending node of the board.
    Methods:

    init: Initializes the board object.
    build_graph: Builds the graph structure of the board.
    add_obstacle: Adds an obstacle to the board.
    remove_obstacle: Removes an obstacle from the board.
    set_start: Sets the starting node of the board.
    set_end: Sets the ending node of the board.
    get_node: Returns the node at a specific location on the board.
    get_neighbors: Returns the neighbors of a given node.
    get_distance: Returns the distance between two nodes on the board.
    is_valid_location: Checks if a location is valid on the board.
    is_valid_move: Checks if a move is valid on the board.
    reset: Resets the board by clearing the visited and last_visited attributes of each node.
    find_shortest_path: Finds the shortest path from the start node to the end node on the board using Dijkstra's algorithm.
    mark_all_paths_found_from_start: Marks all paths from the start node as found.
    mark_all_paths_found_from_here: Marks all paths from a given node as found.
    generate_random_obstacles: Generates a random number of obstacles on the board.
    """
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
        '''
        Initializes a walker object with a start node on the given board at the specified row and column.
        Sets the start node as visited and sets it as the current node.
        Adds the start node to the current path.
        '''
        self.start_node = board[row][col]
        self.start_node.visited = True
        self.current_node = self.start_node
        self.prev_node = None
        self.current_node.visited = True
        self.current_path.append(self.start_node)

    def scan(self):
        '''
        Performs scanning at the current node.
        - If the current node's direction exceeds the number of polygon sides, the end of the path is reached,
        and the current path is appended to the list of paths.
        Then, the walker backtracks, turns right, and scans again.
        If all paths have already been found from the current node, the program exits.
        - If the current node's target at the current direction is None or has been visited,
        the walker turns right and scans again.
        - If the current node's target at the current direction is valid and unvisited,
        the walker moves to that target node, updates the current node and path,
        and scans again.
        '''
        print(f"Scanning Node: [{self.current_node.location.row}][{self.current_node.location.col}] Tgt: {self.current_node.direction}")

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
            print("Moved to Node[{}][{}]".format(
                self.current_node.location.row,
                self.current_node.location.col))
            print("PATH SO FAR:")
            for node in self.current_path:
                print(f"[{node.location.row}],[{node.location.col}] ")
            self.scan()


    def turn_right(self):
        '''
        Turns the walker to the right by incrementing the current node's direction by 1.
        '''
        print(f"Turning RIGHT! [{self.current_node.direction}] -> [{self.current_node.direction + 1}]")
        self.current_node.set_direction(self.current_node.direction + 1)
        print(f"Node[{self.current_node.location.row}][{self.current_node.location.col}] Direction -> {self.current_node.direction}")
    print()


    def move(self):
        '''
        Moves the walker to the next target node in the current direction.
        Updates the previous node to the current node and marks the current node as visited.
        Appends the current node to the current path.
        '''
        self.prev_node = self.current_node
        if self.current_node is not self.start_node:
            self.current_node.last_visited = self.current_node.targets[
                self.current_node.direction]
        self.current_node = self.current_node.targets[
            self.current_node.direction]
        self.current_node.visited = True
        self.current_path.append(copy.deepcopy(self.current_node))


    def backtrack(self):
        '''
        Backtracks the walker to the previous node.
        If the current node is not the start node, pops the last node from the current path and prints
        the updated path.
        If the current path is empty, sets the flag indicating all paths have been found from the start node.
        Prints all the found paths.
        Recursively scans from the current node again.
        '''
        self.current_node = self.prev_node
        print('\n')

        if self.current_node != self.start_node :
            print(f"Backtracking to - [{self.current_path[-1].location.row}][{self.current_path[-1].location.col}] !")
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
            print("\n")
            return
        self.scan()
        return

    def walk(self):
        '''
        Initiates the walker's traversal by scanning and moving to the next node.
        Recursively continues the walking process.
        '''
        self.scan()
        self.move()
        self.walk()

os.system('clear')
b = Board(level)
b.display()
b.show_targets()
w = Walker(b.board, 0, 0)
w.walk()
