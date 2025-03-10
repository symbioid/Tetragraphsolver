from collections import namedtuple
import networkx as nx

G = nx.DiGraph()

direction_matrix = [-1, 1, 1, -1]
# adjacent_direction_inversion = [2, 3, 0, 1]
level = [[2, 1, 1], [1, 1, 2], [1, 1, 2]]
ROW_WIDTH = 3
COL_HEIGHT = 3
NUM_POLY_SIDES = 4
current_path = []
all_paths = [[]]
Location = namedtuple("Location", ["row", "col"])


class Node:
    def __init__(self, value, row, col):
        Location = namedtuple("Location", ["row", "col"])
        self.location = Location(row, col)
        self.ident = f"{row},{col}"
        self.value = value
        self.targets = []
        self.visited = False
        self.direction = 0
        self.visited_by = []

    def __repr__(self):
        return f"{self.ident.split(' ')}"


class Board:
    board = []

    # Make Board
    def __init__(self, level, row, col):
        for r, row in enumerate(level):
            board_row = []
            for c, value in enumerate(row):
                n = Node(value, r, c)
                board_row.append(n)
                G.add_node(n)
            self.board.append(board_row)

        # Add Targets to each Node
        for r in range(COL_HEIGHT):
            for c in range(ROW_WIDTH):
                for i in range(NUM_POLY_SIDES):
                    if (i % 2) == 0:
                        self.target_row = (
                            r + self.board[r][c].value * direction_matrix[i]
                        )
                        self.target_col = c
                    else:
                        self.target_row = r
                        self.target_col = (
                            c + self.board[r][c].value * direction_matrix[i]
                        )
                    if (
                        (self.target_row < 0)
                        or (self.target_row >= COL_HEIGHT)
                        or (self.target_col < 0)
                        or (self.target_col >= ROW_WIDTH)
                    ):
                        pass
                    else:
                        self.board[r][c].targets.append(
                            self.board[self.target_row][self.target_col]
                        )
                        G.add_edge(
                            self.board[r][c],
                            self.board[self.target_row][self.target_col],
                        )

    def display(self, active):
        defaultcolor = "\033[0m"
        activecolor = "\033[33m"
        print("-----------------------")
        print("|   SHOWING BOARD:    |")
        print("-----------------------")
        for row in self.board:
            for node in row:
                if node.location == active.location:
                    print(activecolor + f"{node.value}", end=" ")
                else:
                    print(defaultcolor + f"{node.value}", end=" ")
            print("\033[0m")
        print("-----------------------")

    def show_targets(self):
        for r, row in enumerate(self.board):
            for c, node in enumerate(row):
                for i, t in enumerate(self.board[r][c].targets):
                    print(
                        f"Node [{r}][{c}] -> Target {i} : [{t.location.row}][{t.location.col}] | Value -> {t.value}"
                    )
                print("------------")
        print()


class Walker:
    starting_row = 0
    starting_col = 0

    board = Board(level, starting_row, starting_col)
    current_node = board.board[starting_row][starting_col]

    def __init__(self, board, row):
        self.location = Location(self.starting_row, self.starting_col)
        self.current_node = self.board.board[self.starting_row][self.starting_col]
        self.current_node.visited = True
        self.current_node.visited_by = None
        current_path.append(self.current_node)

    def show_self(self):
        self.board.display(self.current_node)

        print(
            f"walker.current_node.location: {self.current_node.location[0]}, {self.current_node.location[1]}"
        )
        print(f"walker.current_node.value: {self.current_node.value}")
        print("-----------------------")

    def walk(self):
        for target in self.current_node.targets:
            if target.visited is False:
                self.show_self()
                self.visit(target)
                current_path.append(target)

    def visit(self, target):
        print(f"From: {self.current_node.location}")
        self.current_node.visited = True
        self.current_node = target
        print(f"To: {self.current_node.location}")
        self.walk()


w = Walker(0, 1)
# w.board.display(w.current_node)
# w.show_self()
# w.board.show_targets()
# print(G.nodes)
w.walk()
