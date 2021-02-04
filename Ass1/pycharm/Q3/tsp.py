from opentsp.objects import Generator
import numpy as np
from tsp_helper import *
import random
import itertools

# Constants
NUM_TSP_INSTANCES = 100
NUM_CITIES = 7

# Use the OpenTSP library to generate our TSP instances
# Reference: https://pypi.org/project/opentsp/
# Install: pip install opentsp

gen = Generator()  # generator to construct the random TSP instances using opentsp library


# Part A
def partA():
    tsp_lst = []
    for i in range(NUM_TSP_INSTANCES):
        # Generate random TSP instance
        inst = gen.new_instance(NUM_CITIES)

        # Compute the brute force tour cost/length
        tour_cost = computeTourCost(inst)

        # Make an result object to store the random tour info
        tsp_obj = TSPResult(inst, tour_cost)

        # append
        tsp_lst.append(tsp_obj)

    print("\nGenerated %s random instances of TSP, each containing %s cities." % (NUM_TSP_INSTANCES, NUM_CITIES))

    # Compute metrics
    list_of_optimal_tour_costs = [tsp.cost for tsp in tsp_lst]
    mean = np.mean(list_of_optimal_tour_costs)
    min = np.min(list_of_optimal_tour_costs)
    max = np.max(list_of_optimal_tour_costs)
    std = np.std(list_of_optimal_tour_costs)

    # Show metrics
    print("Avg: %8.3f" % mean)
    print("Min: %8.3f" % min)
    print("Max: %8.3f" % max)
    print("Std: %8.3f" % std)


# Part B
def partB():
    tsp_lst = []
    for i in range(NUM_TSP_INSTANCES):

        print("TSP Instance:", i)

        tsp = gen.new_instance(NUM_CITIES)
        print("Created TSP instance")
        if NUM_CITIES > 10:
            out = randomTour(tsp, compute_costs=True, compute_optimal=False)
        else:
            out = randomTour(tsp, compute_costs=True, compute_optimal=True)

        print("Generated random tour")
        tsp_lst.append(out)

    print("\nGenerated %s random instances of TSP, each containing %s cities." % (NUM_TSP_INSTANCES, NUM_CITIES))
    print("Computed the cost of a random tour in each of the %s TSP instances." % NUM_TSP_INSTANCES)

    # Compute metrics
    list_of_optimal_tour_costs = [tsp['random'] for tsp in tsp_lst]
    mean = np.mean(list_of_optimal_tour_costs)
    min = np.min(list_of_optimal_tour_costs)
    max = np.max(list_of_optimal_tour_costs)
    std = np.std(list_of_optimal_tour_costs)

    # Find, if any, the number of tours where the random tour happens to be the optimal tour
    randomIsOptimal = 0
    for t in tsp_lst:
        random_cost = t['random']
        optimal_cost = t['optimal']

        if random_cost == optimal_cost:
            randomIsOptimal += 1

    # Show metrics
    print("Avg: %8.3f" % mean)
    print("Min: %8.3f" % min)
    print("Max: %8.3f" % max)
    print("Std: %8.3f" % std)
    print("-----------------")
    print("Random happens to be optimal: %3d" % randomIsOptimal)


def randomTour(tsp, compute_costs=True, compute_optimal=True):
    cost_random = 0
    cost_optimal = 0;

    # Randomly pick starting point
    random_start_index = random.randrange(len(tsp.nodes_as_list))
    start = tsp.nodes_as_list[random_start_index]
    rest = tsp.nodes_as_list[:random_start_index] + tsp.nodes_as_list[random_start_index + 1:]

    # Construct a random tour

    # sort the remaining points
    r = random.random()
    random.shuffle(rest, lambda: r)

    # put the starting point back
    rest.insert(0, start)

    # return to the starting point
    rest.append(start)

    if compute_costs:
        # Compute cost of the random tour, and optimal tour
        cost_random = computeTourCost(tsp, solve=False, nodes=rest)
        if compute_optimal:
            cost_optimal = computeTourCost(tsp, solve=True)

    return {'random_tour': rest, 'random': cost_random, 'optimal': cost_optimal}


# Part C
def partC():
    tsp_lst = []  # to hold all the costs found by the algorithm
    algo_found_optimal = 0
    optimal_cost = 0

    for i in range(NUM_TSP_INSTANCES):

        print("TSP Instance:", i)

        tsp = gen.new_instance(NUM_CITIES)

        if NUM_CITIES > 10:
            random = randomTour(tsp, compute_costs=True, compute_optimal=False)
        else:
            random = randomTour(tsp, compute_costs=True, compute_optimal=True)

        print("Generated random tour")
        random_tour = random['random_tour']

        # print("Random tour:", random_tour)

        # Construct list of edges to manipulate them in the 2-change neighbourhood function
        random_edges = parseEdges(random_tour)

        # Generate list of all 2-change edge combinations
        all_2_change_combinations = list(itertools.combinations(random_edges, 2))

        # print("Edges:", random_edges)
        # print("Comb:", all_2_change_combinations, "\n")

        neighbour_paths = []
        for edges_comb in all_2_change_combinations:  # this runs (n choose 2) times at each iteration

            neighbour = parseEdges(random_tour)
            # print("Initial path:", neighbour)

            # parse the 2 edges picked at this iteration
            edge1, edge2 = edges_comb

            # make copies of the edge lists so they're not aliases of the original ones (would be affecting our
            # original list of combinations)
            edge1_cpy = edge1.copy()
            edge2_cpy = edge2.copy()

            # print("Edges before:", edge1_cpy, edge2_cpy)

            # save the indeces of the edges to be changed from the original edge list
            edge1_ind = neighbour.index(edge1_cpy)
            edge2_ind = neighbour.index(edge2_cpy)

            # invert the order of the corresponding vertices
            temp = edge1_cpy[1]
            edge1_cpy[1] = edge2_cpy[1]
            edge2_cpy[1] = temp

            # print("Edges after:", edge1_cpy, edge2_cpy)

            # assign the swapped edges to their correct position
            neighbour[edge1_ind] = edge1_cpy
            neighbour[edge2_ind] = edge2_cpy

            # print("2-change:", neighbour)

            # now re-construct the modified random tour node path sequence
            neighbour_p = []
            neighbour_cpy = neighbour.copy()
            i = 0
            while neighbour_cpy:
                e = neighbour_cpy[i]
                start = e[0]
                dest = e[1]
                neighbour_p.append(start)
                neighbour_cpy.pop(i)
                where_to = findNextNodeIndex(neighbour_cpy, dest)
                i = where_to

            # and now just return to start node
            neighbour_p.append(neighbour_p[0])

            # print("Neighbour path:", neighbour_p, "\n")

            # Add it to our list of possible paths found by the algorithm
            neighbour_paths.append(neighbour_p)

        print("Iterated over all 2-change neighbours")

        # print("Generated", len(neighbour_paths), "possible neighbours using 2-change neighbourhood function.")
        # tsp.view(result=None, nodes=True, edges=True)

        # --------------------------------------
        # At this point, we have all the possible paths, derived from the 2-change neighbourhood function
        # Perform our greedy local search

        lowest_cost = computeTourCost(tsp, solve=False, nodes=neighbour_paths[0])
        best_path = neighbour_paths[0]

        if NUM_CITIES <= 10:
            optimal_cost = computeTourCost(tsp, solve=True)

        print("Hill-climbing over neighbours")
        for n in neighbour_paths:
            cost = computeTourCost(tsp, solve=False, nodes=n)
            tsp_lst
            if cost < lowest_cost:
                lowest_cost = cost
                best_path = n

            if lowest_cost == optimal_cost:
                algo_found_optimal += 1

        # Add the best path for this iteration to our list to compute the metrics later on
        tsp_lst.append({'path': best_path, 'cost': lowest_cost})

        # print("")
        # print("Optimal:", optimal_cost)
        # print("Algo:", lowest_cost, best_path)
        # print("Optimal cost found:", algo_found_optimal)

        print("\n")

    # Compute metrics
    list_of_tour_costs = [tsp['cost'] for tsp in tsp_lst]
    mean = np.mean(list_of_tour_costs)
    min = np.min(list_of_tour_costs)
    max = np.max(list_of_tour_costs)
    std = np.std(list_of_tour_costs)

    # Show metrics
    print("Avg: %8.3f" % mean)
    print("Min: %8.3f" % min)
    print("Max: %8.3f" % max)
    print("Std: %8.3f" % std)
    print("-----------------")
    print("Algo found the optimal solution %3d time(s)" % algo_found_optimal)



def findNextNodeIndex(neighbour, dest):
    for n in neighbour:
        if n[0] == dest:
            return neighbour.index(n)
    return -1


def parseEdges(nodes):
    # Construct the list of edges from our initial random tour
    edges = list()
    for i in range(0, len(nodes)):
        if i != 0:
            edges.append(nodes[i - 1:i + 1])
    return edges


# Part D
def partD():
    global NUM_CITIES
    NUM_CITIES = 100
    partB()
    # partC()


# ----------------------


def main():
    # Part A
    # partA()

    # Part B
    # partB()

    # Part C
    # partC()

    # Part D
    partD()


if __name__ == '__main__':
    main()
