from opentsp.objects import Generator
import numpy as np


TSP_INSTANCES = 5 # 100
NUM_CITIES = 7

# Class to model TSP results
class TSPResult:
    def __init__(self, instance, cost):
        self.instance = instance
        self.cost = cost

    def __str__(self):
        return self.instance.view(result=None, nodes=True, edges=True, node_zorder=5, node_color='black', edge_color='grey')

    def nodes(self):
        return self.instance.nodes_as_list

    def tourCost(self):
        nodes = tsp_instance.results['brute_force']
        cost = 0
        for i in range(len(nodes)):
            if i + 1 < len(nodes):
                cost += tsp_instance.edge_length(node_one=nodes[i], node_two=nodes[i + 1])
        return cost


# Use the OpenTSP library to generate our TSP instances
# Reference: https://pypi.org/project/opentsp/
# pip install opentsp
tsp_gen = Generator()
tsp_instance = tsp_gen.new_instance(NUM_CITIES)

print(tsp_instance.solve(brute_force=True))
print(tsp_instance.instance_edge_sum)
print(sum(tsp_instance.edge_lengths_as_list))
print(tsp_instance.results['brute_force'])








