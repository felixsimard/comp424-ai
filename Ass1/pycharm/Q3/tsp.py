from opentsp.objects import Generator
import numpy as np
from tsp_helper import *

# Constants
NUM_TSP_INSTANCES = 100
NUM_CITIES = 7

# Use the OpenTSP library to generate our TSP instances
# Reference: https://pypi.org/project/opentsp/
# Install: pip install opentsp

gen = Generator() # generator to construct the random TSP instances using opentsp library

# Part A
tsp_lst = []
for i in range(NUM_TSP_INSTANCES):

    # Generate random TSP instance
    inst = gen.new_instance(NUM_CITIES)

    # Compute the brute force tour cost/length
    tour_cost = computeBruteForce(inst)

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



# Part C


# Part D
