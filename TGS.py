class Node:
    def __init__(self, value):
        self.value = value
        self.active = True
    def __repr__(self):
        return str(self.value)        

level =  [[2, 1, 2, 2], [2, 2, 2, 1], [1, 1, 1, 2], [1, 2, 3, 1] ]
board = []

for row in level:
    r = []    
    for val in row:
        r.append(Node(val))
    board.append(r)

for row in board:
    for node in row:
        print(node, end=" ")
    print()

# List Comprehension Form
#b = [[Node(col) for col in row] for row in level]
#print(*b[col],sep="\n")

