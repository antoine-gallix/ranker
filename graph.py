import random
import utils
import copy


class Base_Graph:
    """Basic graph with low level operations

    Here are defined operations that manipulate directly internals.
    """

    def __init__(self, elements):
        self.nodes = set(elements)
        self.indexes = {element: i for i, element in enumerate(elements)}
        self.edges = set()

    def __repr__(self):
        r = []
        r.append("---nodes---")
        for node in self.nodes:
            r.append(str(node))
        r.append("---edges---")
        for edge in self.edges:
            r.append(('{} > {}\n'.format(edge[0], edge[1])))
        return '\n'.join(r)

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
            return random.choice(list(self.nodes))
        else:
            return random.sample(list(self.nodes), n)

    # Graph edition

    def add_edge(self, superior_element, inferior_element):
        """Adds an edge between two nodes

        g.add_edge(A,B) := A > B
        """

        self.edges.add((superior_element, inferior_element))

    def remove_node(self, node):
        """Remove a node and all edges referencing it

        returns the original index of the node at graph creation"""

        self.nodes.remove(node)
        self.edges = set([edge for edge in self.edges if node not in edge])
        return self.indexes[node]

    # Node access

    def get_direct_lower_nodes(self, node):
        return [edge[1] for edge in self.edges if edge[0] == node]

    def get_direct_higher_nodes(self, node):
        return [edge[0] for edge in self.edges if edge[1] == node]

    def get_top_nodes(self):
        """Return all nodes that have no better nodes known"""
        all_nodes = set(self.nodes)
        inferior_nodes = set([edge[1] for edge in self.edges])
        return list(all_nodes - inferior_nodes)

    def get_end_nodes(self):
        """Return all nodes that have no worse nodes known"""
        all_nodes = set(self.nodes)
        superior_nodes = set([edge[0] for edge in self.edges])
        return list(all_nodes - superior_nodes)

    def is_top_node(self, node):
        """test if node is a top node"""
        inferior_nodes = set([edge[1] for edge in self.edges])
        return node not in inferior_nodes

    def is_end_node(self, node):
        """test if node is an end node"""
        superior_nodes = set([edge[0] for edge in self.edges])
        return node not in superior_nodes


class Graph(Base_Graph):
    """Graph with higher level operations"""

    def update_graph(self, element_list, rank):
        """Add ranking information to the graph"""
        ordered_elements = utils.reorder(element_list, rank)
        for i in list(range(len(ordered_elements)))[:-1]:
            self.add_edge(
                superior_element=ordered_elements[i],
                inferior_element=ordered_elements[i + 1]
            )
