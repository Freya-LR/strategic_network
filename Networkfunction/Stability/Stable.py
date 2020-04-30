from Networkfunction.Utility.Utilities import Networks, Node, Whole
import networkx as nx


class Stable:
    """
    In social networks, a link between two players is formed only if both of them decide to do so, however either
    of them can make the decision to delete a link without the other player’s approval. The concept of Nash equilibrium
    has a drawback in this case since it does not take into consideration the fact that the players can discuss their
    decisions. To model such a situation a stability concept that takes this fact into account is required. A useful
    stability concept in this case is Pairwise Stability, which accounts for the mutual approval of both players.
    A network is considered pairwise stable if:

        (i) for all ij ∈ g, if u_{i}(g)>=u_{i}(g-ij) and  u_{j}(g)>=u_{j}(g-ij) , and

        (ii) for all ij ∉ g, there is no such situation that if u_{i}(g+ij)>u_{i}(g), then  u_{j}(g+ij)>u_{j}(g);

    We create two functions that in nodes have a link and nodes have no link to separate the whole definition:

        For the nodes have a link, calculate u_{i}(g-ij) and u_{j}(g-ij) when cutting this link, and compare with
         previous u_{i}(g) and u_{j}(g), if the if u_{i}(g)>=u_{i}(g-ij) and  u_{j}(g)>=u_{j}(g-ij) return 1,
         otherwise return 0;

        For the nodes have no link, calculate u_{i}(g+ij) and u_{i}(g+ij) when adding a link which is not in the network
        and then compare previous u_{i}(g) and u_{j}(g),if u_{i}(g+ij)>u_{i}(g), then  u_{j}(g+ij)>u_{j}(g), return 0,
        otherwise return 1.
        """

    def __init__(self, network_matrix, benefit_matrix, cost_matrix):

        self.network_matrix = network_matrix
        self.benefit_matrix = benefit_matrix
        self.cost_matrix = cost_matrix
        self.node = Node(self.network_matrix, self.benefit_matrix, self.cost_matrix)
        self.label = list(self.network_matrix.index.values)

    def __str__(self):
        return "({0},{1},{2},{3},{4})".format(self.network_matrix, self.benefit_matrix, self.cost_matrix,
                                              self.label, self.node)

    def link(self, i, j):
        """
        Create a Network function to define if nodes i and j have a link between each other
           if the matrix satisfies A[i][j] == 1 and A[j][i] == 1 at the same time, they have a link;
           if the matrix satisfies A[i][j] == 0 and A[j][i] == 0 at the same time, they don't have a link;
           else there is a input mistake of the network
        :param i: string node i
        :param j: string node j
        :return: boolean
            if there is a link between i and j
        """
        if self.network_matrix[i][j] == 1 and self.network_matrix[j][i] == 1:
            return True
        elif self.network_matrix[i][j] == 0 and self.network_matrix[j][i] == 0:
            return False
        else:
            print("Network Matrix Input Error")

    def U(self, i):
        """
        get previous utility of node i before delete link ij, Ui
        :param i: string node
        :return: float the node utility
        """
        return self.node.Node(i)

    def Unew_1(self, i):
        """
        For the network that nodes i and j have a link
            creating a new network matrix A1 by deleting the link of ij, by setting the  A1[i][j] = 0 and  A1[j][i] = 0
            then get the new utility of nodes i and j,
            Unew_1(i) = U.Node(A1, B, C, i)
            Unew_1(j) = U.Node(A0, B, C, j)
            if Unew_1(i) <= U(i) and Unew_1(j) <= U(j): then network satisfies pairwise stability
        :param i: string node
        :return: float new utility of node i when deleting link ij, U_i(g-ij)
        """

        A_temp = self.network_matrix

        for j in self.label:
            A_temp[i][j] = 0
            A_temp[j][i] = 0
            newnet1 = Node(A_temp, self.benefit_matrix, self.cost_matrix)
            return newnet1.Node(i)

    def Unew_0(self, i):
        """
        For the network that nodes i and j have no link, adding a link ij
           creating a new network matrix A0 adding the link of ij, by setting the A0[i][j] = 1 and  A0[j][i] = 1
           then get the new utility of nodes i and j,
           Unew_0(i) = U.Node(A0, B, C, i)
           Unew_0(j) = U.Node(A0, B, C, j)
           if  U(i) < Unew_0(i) and U(j) < Unew_0(j): then network does not satisfy pairwise stability
        :param i: string node
        :return: float new utility of node i when adding link ij, U_i(g-ij)
        """

        A_temp = self.network_matrix

        for j in self.label:
            A_temp[i][j] = 0
            A_temp[j][i] = 0
            newnet0 = Node(A_temp, self.benefit_matrix, self.cost_matrix)
            return newnet0.Node(i)

    def stable_if_link_pair(self):
        """
        Evaluate the first part of pairwise stable when there is a link between note u and v
        :return: boolean
        """
        U_temp = self.Unew_1
        for i in self.label:
            for j in self.label:
                while self.link(i, j) is True:

                    if U_temp(i) >= self.U(i) and U_temp(j) >= self.U(j):
                        # if both utility decrease, it satisfy the first part of pairwise
                        return 1
                    else:
                        return 0

    def stable_if_non_link(self):
        """
        Evaluate the second part of pairwise stable when there is a link between note u and v
        :return: boolean
        """
        U_temp = self.Unew_0
        for i in self.label:
            for j in self.label:
                while self.link(i, j) is False:
                    if U_temp(i) >= self.U(i) and U_temp(j) >= self.U(j):
                        return 0
                    else:
                        return 1  # if both utility not increase at the same time then satisfy the second part of pairwise

    def stable(self):
        """
        When the network has the two attributes linkpair(i,j)=1 and nonlinkpair(i,j) at the same time,
            it is pairwise stable, otherwise it's unstable
        :return: boolean
        """

        if self.stable_if_link_pair() == 1 and self.stable_if_non_link() == 1:
            print("This network is Stable")
            return True
        else:
            print("This network is not Stable")
            return False

    def __repr__(self):
        return 'stability: '


def main():
    network_matrix =input()
    benefit_matrix = input()
    cost_matrix = input()

    return Stable(network_matrix, benefit_matrix, cost_matrix)


if __name__ == '__main__':
    main()
