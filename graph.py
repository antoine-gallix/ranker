import random
import utils
import copy


class Base_Graph:
    """Basic graph with low level operations

    Here are defined operations that manipulate directly internals.
    """

    def __init__(self, elements):
        self.nodes = copy.copy(elements)
        self.indexes = {element: i for i, element in enumerate(elements)}
        self.edges = []

    def __contains__(self, node):
        return node in self.nodes

    def size(self):
        return len(self.nodes)

    def edge_count(self):
        return len(self.edges)

    def get_nodes(self, n):
        """get random nodes

        for testing purposes
        """
        if n == 1:
            return random.choice(self.nodes)
        else:
            return random.sample(self.nodes, n)

    # Graph edition

    def add_edge(self, superior_element, inferior_element):
        """Adds an edge between two nodes"""

        self.edges.append((inferior_element, superior_element))

    def remove_node(self, node):
        """Remove a node and all edges referencing it

        returns the original index of the node at graph creation"""

        self.nodes.remove(node)
        self.edges = [edge for edge in self.edges if node not in edge]
        return self.indexes[node]

    # Node access

    def get_direct_lower_nodes(self, node):
        return [edge[0] for edge in self.edges if edge[1] == node]

    def get_direct_higher_nodes(self, node):
        return [edge[1] for edge in self.edges if edge[0] == node]

    def get_top_nodes(self):
        """Return all nodes that have no better nodes known"""

        return set(self.nodes) - set([edge[0] for edge in self.edges])

    def get_end_nodes(self):
        """Return all nodes that have no worse nodes known"""

        return set(self.nodes) - set([edge[1] for edge in self.edges])


class Graph(Base_Graph):
    """Graph with higher level operations"""

    def update_graph(self, element_list, rank):
        """Add ranking information to the graph"""
        ordered_elements = utils.reorder(element_list, rank)
        for i in list(range(len(ordered_elements)))[1:]:
            self.add_edge(
                superior_element=ordered_elements[i - 1],
                inferior_element=ordered_elements[i]
            )
