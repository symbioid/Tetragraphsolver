from collections import namedtuple

# from turtle import clearscreen

# import copy

# import os
# import sys
import networkx as nx

# from networkx.algorithms import tournament

G = nx.DiGraph()

direction_matrix = [-1, 1, 1, -1]
adjacent_direction_inversion = [2, 3, 0, 1]
level = [[2, 1, 1], [1, 1, 2], [1, 1, 2]]
ROW_WIDTH = 3
COL_HEIGHT = 3
NUM_POLY_SIDES = 4
current_path = []
all_paths = [[]]


class Node:
    def __init__(self, value, row, col):
        Location = namedtuple("Location", ["row", "col"])
        self.location = Location(row, col)
        self.ident = f"{row},{col}"
        self.value = value
        self.targets = []
        self.visited = False
        self.last_visited_direction = 0

    def __repr__(self):
        return f"{self.ident.split(' ')}"


class Board:
    board = []
    target_row = 0
    target_col = 0

    # Make Board
    def __init__(self, level):
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

    def display(self):
        for row in self.board:
            for val in row:
                # print(*row)
                print(val, end=" ")
            print()

    def show_targets(self):
        for r, row in enumerate(self.board):
            for c, node in enumerate(row):
                for i, t in enumerate(self.board[r][c].targets):
                    print(
                        f"Node [{r}][{c}] -> Target {i} : [{t.location.row}][{t.location.col}] | Value -> {t.value}"
                    )
                print("------------")


b = Board(level)
b.display()
b.show_targets()
print(G.nodes)
for line in nx.generate_adjlist(G):
    print(line)
