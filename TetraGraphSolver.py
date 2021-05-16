from collections import namedtuple

class Node:
    def __init__(self, value, r, c):
        self.value = value
        self.visited = False
        self.targets = []
        Location = namedtuple('Location', ['row','col'] )
        self.location = Location(r,c)
        self.lastdirection = 0

    def __repr__(self):
        return str(self.value)

class Board:
    board = []
    def __init__(self, levelname):
        # Make Board
        for r,row in enumerate(levelname):
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
            print(*row)

#---------------------------------------------------------------------------------

class Walker:
    current_node = None
    current_target = None
    index = 0

    def __init__(self, start_node):
        self.current_node = start_node
        self.current_node.visited = True
        self.current_target = start_node.targets[self.index]
    def display(self):
        print ("Current Node = [{}, {}], with Value of '{}'".format(self.current_node.location.row, self.current_node.location.col, self.current_node.value))
        for target in self.current_node.targets:
            if target == None:
                print("None")
            else:
                print("Current Target {}, Current Value: {}".format(target.location, target.value))
    def scan(self):
    	print("New Target = {}".format(self.current_node.targets[self.index].location))
    	if self.current_target == None:
    		print("None") #pass/return/break
    	elif self.current_target.visited == True:
    	    print("Already visited : {}".format(self.current_target.location))
    	else:
    	    self.visit()
    	#self.index += 1
    	#print("New Target = {}".format(self.current_node.targets[self.index]))

    def visit(self):
        self.current_node.lastdirection += 1
        self.current_node = self.current_target #focus on this next...
        self.current_node.visited = True
        self.current_target = self.current_node.targets[self.current_node.lastdirection]
#---------------------------------------------------------------------------------

solutions =[]

direction_matrix = [-1, 1, 1, -1]
level =  [[2, 2, 2, 1], [2, 1, 1, 1], [1, 2, 2, 1], [2, 1, 1, 2]]

b = Board(level)
w = Walker(b.board[3][3])

b.display()
w.display()
w.scan()
w.display()
