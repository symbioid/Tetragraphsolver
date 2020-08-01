from collections import namedtuple
class Node:
    def __init__(self, value):
        self.value = value
        self.active = True
        self.targets = [self.value * target_matrix[i] for i in range(4)]
        self.location = namedtuple('Point', ['x','y'] )
    
    def __repr__(self):
        return str(self.value)    

    #def add_targets(self, board):        
    #    for i in range(4):            
    #        self.targets[i] = self.value * target_matrix[i]

# clockwise: up, right, down, left
# multiply matrix by node value to determine target node to assign to targets list
target_matrix = [-1, 1, 1, -1]

level =  [[2, 1, 2, 2], [2, 2, 2, 1], [1, 1, 1, 2], [1, 2, 3, 1] ]
board = [[Node(col) for col in row] for row in level]



for row in board:
    for node in row:
        print(node, end=" ")
    print()

#for row in board:    
#    for node in row:
#        print(node, ":")
#        for i in range(4):
#            print(node.targets[i], end=",")
#        print()
        
