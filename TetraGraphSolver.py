from collections import namedtuple

class Node:
    def __init__(self, value, r, c):
        self.value = value
        self.visited = False
        self.targets = []
        Location = namedtuple('Locaton', ['row','col'] )
        self.location = Location(r,c)

    def __repr__(self):
        return str(self.value)

class Board:
    board = []
    def __init__(self, level):
        # Make Board
        for r,row in enumerate(level):
            board_row = []
            for c,value in enumerate(row):
                board_row.append(Node(value, r, c))
            self.board.append(board_row)
        # Add Targets to each Node
        for row in self.board:
            for node in row:
                for i in range(4):
                    row_displaced = node.location.row + node.value * direction_matrix[i]
                    col_displaced = node.location.col + node.value * direction_matrix[i]
                    if (row_displaced < 0) or (row_displaced > 3) or (col_displaced < 0 ) or (col_displaced > 3):
                        node.targets.append(None)
                    elif i % 2 == 0:
                        node.targets.append(self.board[row_displaced][node.location.col])
                    else:
                        node.targets.append(self.board[node.location.row][col_displaced])
    def display(self):
        # Display Node Info
        for row in self.board:
            for node in row:
                print("----------------")
                print("Node ({},{}) = [{}] :".format(node.location.row, node.location.col, node))
                print("----------------")
                for i, target in enumerate(node.targets):
                    if target is None:
                        print ("Target {}: (NONE)".format(i))
                    else:
                        print("Target {}: ({},{})".format(i, target.location.row, target.location.col))
                print("----------------")

class Walker:
    current_node = None
    def __init__(self, start_node):
        self.current_node = start_node
    
    def display(self):
        print ("Current Node = [{}, {}], with Value of '{}'".format(self.current_node.location.row, self.current_node.location.col, self.current_node.value))
        for target in self.current_node.targets:
            if target == None:
                print("None")
            else:
                print("Current Value: {}, Current Target {}".format(target.value, target.location))

direction_matrix = [-1, 1, 1, -1]
level =  [[2, 2, 2, 1], [2, 1, 1, 1], [1, 2, 2, 1], [2, 1, 1, 2]]

b = Board(level)
w = Walker(b.board[3][3])

b.display()
w.display()
