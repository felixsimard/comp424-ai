# Class to model TSP results
class TSPResult:
    def __init__(self, instance, cost):
        self.instance = instance
        self.cost = cost

    def view(self):
        return self.instance.view(result=None, nodes=True, edges=True, node_zorder=5, node_color='black', edge_color='grey')

    def nodes(self):
        return self.instance.nodes_as_list

def computeBruteForce(tsp_instance):
    tsp_instance.solve(brute_force=True)
    nodes = tsp_instance.results['brute_force']
    cost = 0
    for i in range(len(nodes)):
        if i + 1 < len(nodes):
            cost += tsp_instance.edge_length(node_one=nodes[i], node_two=nodes[i + 1])
    return cost