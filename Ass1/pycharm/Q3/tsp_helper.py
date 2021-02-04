# Class to model TSP results
class TSPResult:
    def __init__(self, instance, cost):
        self.instance = instance
        self.cost = cost

    def view(self):
        return self.instance.view(result=None, nodes=True, edges=True, node_zorder=5, node_color='black',
                                  edge_color='grey')

    def nodes(self):
        return self.instance.nodes_as_list


def computeTourCost(tsp_instance, solve=True, nodes=[]):
    if solve:
        tsp_instance.solve(brute_force=True)
        nodes = tsp_instance.results['brute_force']
    cost = 0
    for i in range(len(nodes)):
        if i + 1 < len(nodes):
            cost += tsp_instance.edge_length(node_one=nodes[i], node_two=nodes[i + 1])
    return cost

'''
Given the requirements for question 3, 
it does not specify that we need to implement brute_force ourselves, we can rely on some library orr other resource 
to do the computation. We only need to explicitly implement hill climbing/greedy local search.

For brute force, the code would essentially look like this:

def bruteForce(tsp_inst):
    # Generate all possible tour lists
    possible_tours = list(itertools.permutations(tsp_inst))
    tours = []
    for t in possible_tours:
        tour = list(t)
        tour.append(tour[0])
        tours.append(tour)
    tours_costs = []
    # Exhaustively compute all tour lengths and return the minimum
    for t in tours:
        c = # compute tour cost
        tours_costs.append(c)
    
    return min(tours_costs)

'''
