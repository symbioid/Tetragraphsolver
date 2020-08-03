from collections import namedtuple

class Node:
    def __init__(self, value, r, c):
        self.value = value
        self.active = True
        self.targets = []
        Position = namedtuple('Position', ['row','col'] )
        self.location = Position(r,c)
    
    def __repr__(self):
        return str(self.value)    

direction_matrix = [-1, 1, 1, -1]
level =  [[2, 2, 2, 1], [2, 1, 1, 1], [1, 2, 2, 1], [2, 1, 1, 2]]

board = []

# Make Board
for r,row in enumerate(level):
    board_row = []
    for c,value in enumerate(row):
        board_row.append(Node(value, r, c))
    board.append(board_row)

# Add Targets to each Node
for row in board:
    for node in row:
        for i in range(4):            
            row_displaced = node.location.row + node.value * direction_matrix[i]
            col_displaced = node.location.col + node.value * direction_matrix[i]
            if (row_displaced < 0) or (row_displaced > 3) or (col_displaced < 0 ) or (col_displaced > 3):
                node.targets.append(None)
            elif i % 2 == 0:                
                node.targets.append(board[row_displaced][node.location.col])
            else:                                
                node.targets.append(board[node.location.row][col_displaced])                        

# Display Node Info
for row in board:    
    for node in row:
        print("----------------")
        print("Node ({},{}) = [{}] :".format(node.location.row, node.location.col, node))
        print("----------------")
        for i, target in enumerate(node.targets):
            if target is None:
                print ("Target {}: (NONE)".format(i))                
            else:
                print("Target {}: ({},{})".format(i, target.location.row, target.location.col))                   
    