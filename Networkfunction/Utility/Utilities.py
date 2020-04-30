import networkx as nx
import numpy as np
import pandas as pd


class Networks:

    """
    create a Networkfunction of the benefit of each node to calculate the utility of nodes
    when the distance between nodes less than dmax, and each benefit larger than one,
    It's direct connection when connection distance is 1, and it's indirect connection
     when connection distance is larger than 1;
    (1) calculate the benefit of nodes that distance is 1 ---- number*b(1)
    (2) calculate the benefit of nodes that distance is 2 ---- numbers*b(2)
    ...
    (n) calculate the benefit of nodes that distance is dmax ---- numbers*b(dmax)
    (n+1) sum all the results ---- the total benefit every node get from the whole network
    """

    def __init__(self, network_matrix, benefit_matrix, cost_matrix):
        """
        :param network_matrix: matrix
               matrix including information of nodes and links
        :param benefit_matrix: matrix
               matrix including information of distance and benefits
        :param cost_matrix:  matrix
               matrix including information of cost betwwen each pair of nodes
        """
        self.network_matrix = network_matrix
        self.benefit_matrix = benefit_matrix
        self.cost_matrix = cost_matrix
        self.g = nx.Graph(self.network_matrix)  # generate a network using matrix
        self.n = nx.number_of_nodes(self.g)  # the number of nodes in the network
        """
        for every node i, connect list is the distance list from all nodes to i,
        i is like:     {
               'A': {'A': 0, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'G': 1, 'F': 2, 'H': 2, 'I': 3, 'J': 4},
               'B': {'B': 0, 'A': 1, 'D': 1, 'E': 1, 'F': 1, 'C': 2, 'G': 2, 'H': 3, 'I': 4, 'J': 5},
               'C': {'C': 0, 'A': 1, 'D': 1, 'E': 1, 'H': 1, 'B': 2, 'G': 2, 'I': 2, 'F': 3, 'J': 3},
               'D': {'D': 0, 'A': 1, 'B': 1, 'C': 1, 'E': 1, 'G': 2, 'F': 2, 'H': 2, 'I': 3, 'J': 4},
               'E': {'E': 0, 'A': 1, 'B': 1, 'C': 1, 'D': 1, 'G': 2, 'F': 2, 'H': 2, 'I': 3, 'J': 4},
               'F': {'F': 0, 'B': 1, 'A': 2, 'D': 2, 'E': 2, 'C': 3, 'G': 3, 'H': 4, 'I': 5, 'J': 6},
               'G': {'G': 0, 'A': 1, 'B': 2, 'C': 2, 'D': 2, 'E': 2, 'F': 3, 'H': 3, 'I': 4, 'J': 5},
               'H': {'H': 0, 'C': 1, 'I': 1, 'A': 2, 'D': 2, 'E': 2, 'J': 2, 'B': 3, 'G': 3, 'F': 4},
               'I': {'I': 0, 'H': 1, 'J': 1, 'C': 2, 'A': 3, 'D': 3, 'E': 3, 'B': 4, 'G': 4, 'F': 5},
               'J': {'J': 0, 'I': 1, 'H': 2, 'C': 3, 'A': 4, 'D': 4, 'E': 4, 'B': 5, 'G': 5, 'F': 6}
               }
            """
        self.distance = dict(nx.all_pairs_shortest_path_length(self.g))

        self.label = self.g.nodes()  # the label of the nodes in the network

    def __str__(self):
        return "({0},{1},{2},{3},{4})".format(self.network_matrix, self.benefit_matrix,self.cost_matrix,
                                          self.label, self.dmax)

    def number(self, node, d):  # node is a specific node name, d is the determined distance we need
        """
        :param node: string
            given node
        :param d: int
            specific distance
        :return: int
            number of different distance from 0 to dmax
        """
        self.count = 0  # count the number of different distance from a specific node
        l = self.distance[node]  # the distance list of node[node]
        for k in self.label:  # for the other node in the network
            if d == l[k]:  # if the key in the distance is what we need
                self.count += 1  # count 1 for this time

        return self.count  # return the total number of given node and distance

    def NodeU(self):
        """
        :return: float
            the utility list of all nodes
        """
        self.dmax = nx.algorithms.distance_measures.diameter(self.g)
        # the diameter of the network is the maximum distance of two nodes in network
        self.ub = []

        for i in self.label:  # for each node i
            costmul = pd.DataFrame.multiply(self.network_matrix, self.cost_matrix, axis=0)
            total_cost = pd.DataFrame.sum(costmul, axis=0)
            self.cost=total_cost[i]   # the cost of each node i is the
            # cost of direct connections between node i to node j, which equal to production of row i
            # in network matrix and cost matrix
            self.Be = 0
            d = 0
            while d <= self.dmax:  # when the distance is larger than dmax, exit execute from loop

                self.Be += self.number(i, d) * self.benefit_matrix[d]  # benefits sum of distance from 0 to dmax
                d += 1  # distance +1 every time until key=dmax

            self.ub.append(self.Be - self.cost[0])  # the difference of total benefits and total costs of each node
        return self.ub  # return the list of utility of each node

    def __repr__(self):
        return 'Node n:' + str(self.ub)


class Node(Networks):

    """
    get benefit of a given node n
    """
    def __init__(self, network_matrix, benefit_matrix, cost_matrix):
        super().__init__(network_matrix, benefit_matrix, cost_matrix)
        self.network_matrix = network_matrix
        self.benefit_matrix = benefit_matrix
        self.cost_matrix = cost_matrix

    def __str__(self):
        return "({0},{1},{2})".format(self.network_matrix, self.benefit_matrix, self.cost_matrix)

    def Node(self, noden):
        """
        :param noden: string
            a given node
        :return: float
            utility of this node
        """
        self.net = Networks(self.network_matrix, self.benefit_matrix, self.cost_matrix)
        getloc=self.network_matrix.index.get_loc(noden) # get the location of node (int)
        self.Nodei = self.net.NodeU()[getloc]
        return self.Nodei

    def __repr__(self):
        return str(self.Nodei)


class Whole(Node):
    """
    Calculate the total utility of the network
    """
    def __init__(self, network_matrix, benefit_matrix, cost_matrix):
        super().__init__(network_matrix, benefit_matrix, cost_matrix)
        self.network_matrix = network_matrix
        self.benefit_matrix = benefit_matrix
        self.cost_matrix = cost_matrix
        self.ut = 0

    def __str__(self):
        return "({0},{1},{2},{3})".format(self.network_matrix, self.benefit_matrix, self.cost_matrix, self.ut)

    def wholeutility(self):
        """
        :return: float
            total utility of this network
        """
        self.no = Node(self.network_matrix, self.benefit_matrix, self.cost_matrix)
        for i in self.no.label:
            self.ut += self.no.Node(i)
        return self.ut

    def __repr__(self):
        return 'wholeutility:' + str(self.ut)


if __name__ == '__main__':
   main()
