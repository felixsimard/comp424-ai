from sixpuzzle import *

BOARD_LEN = 3

# Reference: https://github.com/speix/8-puzzle-solver

# Representing a 'State'
class State:
    def __init__(self, state, parent, move, moved, depth, cost):
        self.state = state
        self.parent = parent
        self.move = move
        self.moved = moved
        self.depth = depth
        self.cost = cost
        if self.state:
            self.map = ''.join(str(e) for e in self.state)  # say, [1, 4, 2, 5, 3, 0] becomes '142530'

    def __eq__(self, other):  # override equality check for comparing two state
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map

    def __str__(self):
        pieces = self.state
        out = ''
        for i in range(0, len(pieces)):
            if i == 0:
                out += '-------------\n'
            out = out + '| {0:d} '.format(pieces[i])
            if (i + 1) % BOARD_LEN == 0:
                out = out + '|' + '\n' + '-------------\n'
        return out

# Generate children
def expandChildren(node):
    neighbors = []

    # Up
    moved_piece, new_state = move(node.state, 1)
    neighbors.append(State(new_state, node, 1, moved_piece, node.depth + 1, node.cost + 1))

    # Down
    moved_piece, new_state = move(node.state, 2)
    neighbors.append(State(new_state, node, 2, moved_piece, node.depth + 1, node.cost + 1))

    # Left
    moved_piece, new_state = move(node.state, 3)
    neighbors.append(State(new_state, node, 3, moved_piece, node.depth + 1, node.cost + 1))

    # Right
    moved_piece, new_state = move(node.state, 4)
    neighbors.append(State(new_state, node, 4, moved_piece, node.depth + 1, node.cost + 1))

    nodes = [neighbor for neighbor in neighbors if neighbor.state]

    return nodes


# Move a piece
def move(state, direction):
    new_state = state[:]  # makes a copy of current board configuration

    index = new_state.index(0)

    if index == 0:  # Moving top-left piece
        if direction == 1:
            return 100, None
        if direction == 2:
            temp = new_state[0]
            moved = new_state[3]
            new_state[0] = new_state[3]  # 3 as in the index of the piece right below the top leftmost piece
            new_state[3] = temp
            return moved, new_state
        if direction == 3:
            return 100, None
        if direction == 4:
            temp = new_state[0]
            moved = new_state[1]
            new_state[0] = new_state[1]
            new_state[1] = temp
            return moved, new_state

    if index == 1:  # Moving top-middle piece
        if direction == 1:
            return 100, None
        if direction == 2:
            temp = new_state[1]
            moved = new_state[4]
            new_state[1] = new_state[4]
            new_state[4] = temp
            return moved, new_state
        if direction == 3:
            temp = new_state[1]
            moved = new_state[0]
            new_state[1] = new_state[0]
            new_state[0] = temp
            return moved, new_state
        if direction == 4:
            temp = new_state[1]
            moved = new_state[2]
            new_state[1] = new_state[2]
            new_state[2] = temp
            return moved, new_state

    if index == 2:  # Moving top-right piece
        if direction == 1:
            return 100, None
        if direction == 2:
            temp = new_state[2]
            moved = new_state[5]
            new_state[2] = new_state[5]
            new_state[5] = temp
            return moved, new_state
        if direction == 3:
            temp = new_state[2]
            moved = new_state[1]
            new_state[2] = new_state[1]
            new_state[1] = temp
            return moved, new_state
        if direction == 4:
            return 100, None

    if index == 3:  # Moving bottom-left piece
        if direction == 1:
            temp = new_state[3]
            moved = new_state[0]
            new_state[3] = new_state[0]
            new_state[0] = temp
            return moved, new_state
        if direction == 2:
            return 100, None
        if direction == 3:
            return 100, None
        if direction == 4:
            temp = new_state[3]
            moved = new_state[4]
            new_state[3] = new_state[4]
            new_state[4] = temp
            return moved, new_state

    if index == 4:  # Moving bottom-middle piece
        if direction == 1:
            temp = new_state[4]
            moved = new_state[1]
            new_state[4] = new_state[1]
            new_state[1] = temp
            return moved, new_state
        if direction == 2:
            return 100, None
        if direction == 3:
            temp = new_state[4]
            moved = new_state[3]
            new_state[4] = new_state[3]
            new_state[3] = temp
            return moved, new_state
        if direction == 4:
            temp = new_state[4]
            moved = new_state[5]
            new_state[4] = new_state[5]
            new_state[5] = temp
            return moved, new_state

    if index == 5:  # Moving bottom-right piece
        if direction == 1:
            temp = new_state[5]
            moved = new_state[2]
            new_state[5] = new_state[2]
            new_state[2] = temp
            return moved, new_state
        if direction == 2:
            return 100, None
        if direction == 3:
            temp = new_state[5]
            moved = new_state[4]
            new_state[5] = new_state[4]
            new_state[4] = temp
            return moved, new_state
        if direction == 4:
            return 100, None
