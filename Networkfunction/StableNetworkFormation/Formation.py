from Networkfunction.Utility.Utilities import Whole, Node, Networks
from Networkfunction.Stability.Stable import Stable
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Formation:
    """
    If the network is not stable, its stable form should be found by changing its link state each time,
    (1) for the tow nodes who has a link, if the utility of each node is larger than previous one after cutting
        the link, then this link should be cut to form a more stable network.
    (2) for the tow nodes who has no link, if the utility of each node is larger than previous one after adding
        the link, then this link should be add to form a more stable network.
    (3) test stability after changing link each time, execute the new network if it's stable,
     otherwise continue changing loop
    """

    def __init__(self, network_matrix, benefit_matrix, cost_matrix):

        self.network_matrix = network_matrix
        self.benefit_matrix = benefit_matrix
        self.cost_matrix = cost_matrix
        self.network = Networks(self.network_matrix, self.benefit_matrix, self.cost_matrix)
        self.ndoe = Node(self.network_matrix, self.benefit_matrix, self.cost_matrix)
        self.s = Stable(self.network_matrix, self.benefit_matrix, self.cost_matrix)

    def __str__(self):
        return "({0},{1},{2})".format(self.network_matrix, self.benefit_matrix, self.cost_matrix)

    def get_newnetwork(self, m, i, j):
        """
        this function is to get a new network matrix which has better stability testing the utility
        :param m: matrix which is need to reformed
        :param i: string node i
        :param j: string node j
        :return: matrix that is more stable than matrix m
        """

        self.new_matrix = m
        self.sa = Stable(m, self.benefit_matrix, self.cost_matrix)

        while self.sa.link(i, j) is True:  # the link is in this network, cut the link
            U_temp = self.sa.Unew_1
            if U_temp(i) >= self.sa.U(i) and U_temp(j) >= self.sa.U(j):
                # if both utility decrease, it satisfy the first part of pairwise
                self.new_matrix[i][j] = 0
                self.new_matrix[j][i] = 0
        else:
            U_temp = self.sa.Unew_0
            if U_temp(i) >= self.sa.U(i) and U_temp(j) >= self.sa.U(j):
                # if both utility decrease, it satisfy the first part of pairwise
                self.new_matrix[i][j] = 1
                self.new_matrix[j][i] = 1
        return self.new_matrix

    def decide(self):
        """
        if the new network is stable, then we have a stable network,
        else, format the network again using function get_newnetwork() and run another test loop
        the stable network may not be unique
        :return: matrix describe the stable networks
        """
        for i in self.network.label:
            for j in self.network.label:
                self.get = self.get_newnetwork(self.network_matrix, i, j)

                while Stable(self.get,self.benefit_matrix,self.cost_matrix) is False:
                    self.final = self.get_newnetwork(self.get, i, j)
                    return self.final
                else:
                    self.final = self.get
                    return self.final

    def __repr__(self):
        return 'The stable network is : ' + str(self.final)

def main():
    network_matrix = input()
    benefit_matrix = input()
    cost_matrix = input()
    F = Formation(network_matrix, benefit_matrix, cost_matrix)
    return F.decide()


if __name__ == '__main__':

  main()

