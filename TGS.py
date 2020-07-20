

class Node:
    def __init__(self, value):
        self.value = value
        self.active = True
    def show(self):
        print(self.value, end=" ")

level =  [[2, 1, 2, 2], [2, 2, 2, 1], [1, 1, 1, 2], [1, 2, 3, 1] ]

board = []
for i in range(len(level)):
    board.append([])    
    for j in range(len(level[i])):
        board[i].append(Node(level[i][j]))        
        board[i][j].show()
    print()