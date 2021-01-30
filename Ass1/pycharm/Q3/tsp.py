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
        tsp = gen.new_instance(NUM_CITIES)
        out = randomTour(tsp)
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
        random_cost = round(t['random'])
        optimal_cost = round(t['optimal'])

        if random_cost == optimal_cost:
            randomIsOptimal += 1

    # Show metrics
    print("Avg: %8.3f" % mean)
    print("Min: %8.3f" % min)
    print("Max: %8.3f" % max)
    print("Std: %8.3f" % std)
    print("-----------------")
    print("Random happens to be optimal: %3d" % randomIsOptimal)


def randomTour(tsp, compute_costs=True):

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
        cost_optimal = computeTourCost(tsp, solve=True)

    return {'random_tour': rest, 'random': cost_random, 'optimal': cost_optimal}


# Part C
def partC():

    tsp = gen.new_instance(NUM_CITIES)
    random = randomTour(tsp, compute_costs=True)
    random_tour = random['random_tour']

    print("Random tour:", random_tour)

    num_pairings = len(random_tour) / 2
    all_2_change_combinations = list(itertools.combinations(random_tour, 2))
    #print(all_2_change_combinations)
    #print(len(all_2_change_combinations))
    print(tsp.edges)



    tsp.view(result=None, nodes=True, edges=True)

# Part D


# ----------------------


def main():
    # Part A
    # partA()

    # Part B
    # partB()

    # Part C
    partC()

    # Part D


if __name__ == '__main__':
    main()
