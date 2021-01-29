from collections import deque
from helper import *
from queue import PriorityQueue

# Reference used a building ground and inspiration
# https://github.com/speix/8-puzzle-solver

# Initial and goal states
# Note: we represent the empty tile as a '0'
initial_state = [1, 4, 2, 5, 3, 0]
goal_state = [0, 1, 2, 5, 4, 3]

# global variable to store goal node through each algorithm used
goal_node = None

moves = {
    1: "Up",
    2: "Down",
    3: "Left",
    4: "Right"
}


# ----------------------------------------------

# BFS

def bfs(init_state):
    global goal_node

    explored = set()

    start_state = State(init_state, None, None, 0, 0, 0)
    q = deque([start_state])

    print("Start state:")
    print(start_state)

    while q:
        node = q.popleft()

        explored.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return q

        neighbors = expandChildren(node)
        neighbors.sort(key=lambda s: s.moved)

        for n in neighbors:
            if n.map not in explored:
                q.append(n)
                explored.add(n.map)


# ----------------------------------------------

# Uniform Cost Search

def ucs(init_state):
    global goal_node

    explored = set()

    q = PriorityQueue()
    start_state = State(init_state, None, None, 0, 0, 0)
    q.put((0, start_state))

    print("Start state:")
    print(start_state)

    while q:

        pq_priority, node = q.get()

        explored.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return q

        neighbors = expandChildren(node)

        for n in neighbors:
            if n.map not in explored:
                q.put((n.cost, n))
                explored.add(n.map)


# ----------------------------------------------

# DFS

def dfs(init_state):
    global goal_node

    explored = set()
    start_state = State(init_state, None, None, 0, 0, 0)
    stack = list([start_state])

    print("Start state:")
    print(start_state)

    while stack:

        node = stack.pop()
        explored.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return stack

        neighbors = expandChildren(node)
        neighbors.sort(key=lambda s: s.moved, reverse=True)

        for neighbor in neighbors:
            if neighbor.map not in explored and neighbor not in stack:
                stack.append(neighbor)
                explored.add(neighbor.map)


# ----------------------------------------------


# Iterative Deepening Search

# Make a depth-limited search helper function
def dls(explored, stack, max_depth):

    global goal_node
    node = stack.pop()
    explored.add(node.map)

    # If found the goal state
    if node.state == goal_state:
        goal_node = node
        return True

    # If reached maximum depth
    if max_depth <= 0:
        return False

    # Get neighbors
    neighbors = expandChildren(node)
    neighbors.sort(key=lambda s: s.moved, reverse=True)

    for neighbor in neighbors:
        if neighbor.map not in explored and neighbor not in stack:
            stack.append(neighbor)
            explored.add(neighbor.map)
            if dls(explored, stack, max_depth-1): # recursive dls
                return True

    return False

def ids(init_state):

    global goal_node
    max_depth = 5

    explored = set()
    start_state = State(init_state, None, None, 0, 0, 0)
    stack = list([start_state])

    print("Start state:")
    print(start_state)

    for i in range(max_depth):
        if dls(explored, stack, max_depth):
            print("IDS: Solution found.")
            return True

    print("IDS: No solution found.")
    return False

# ----------------------------------------------


def showSolution():
    global goal_node
    global moves
    ops = []
    while initial_state != goal_node.state:
        op = (moves[goal_node.move], goal_node)
        ops.insert(0, op)
        goal_node = goal_node.parent

    for o in ops:
        move, state = o
        #print(state.state, end=' -> ')
        print(move, "\n", state)
    print("Goal state reached in", len(ops), "moves", "\n\n")


# MAIN

def main():

    # print("-------------------------")
    # print("BFS")
    # print("-------------------------")
    #
    # # BFS
    # bfs(initial_state)
    # showSolution()

    # print("-------------------------")
    # print("Uniform Cost Search")
    # print("-------------------------")
    #
    # # Uniform cost search
    # ucs(initial_state)
    # showSolution()

    print("-------------------------")
    print("DFS")
    print("-------------------------")

    # DFS
    dfs(initial_state)
    showSolution()


    # print("-------------------------")
    # print("Iterative Deepening Search")
    # print("-------------------------")
    #
    # # Iterative deepening
    # ids(initial_state)
    # showSolution()


if __name__ == '__main__':
    main()
