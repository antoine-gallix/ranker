import utils
import base_lib


def rank_elements(element_set, version=0):
    g = ranker_graph(element_set)
    return g.rank_elements(version=version)


class ranker_graph:
    """data structure that record ranking relation between elements

    the internal structure is a dict whose keys are elements and values are set of element we know are directly better than the given element.
    """

    def __init__(self, element_list):
        self.element_list = element_list
        self.graph = {element: set() for element in element_list}

    def __repr__(self):
        r = ""
        for k, v in self.graph.items():
            r += ('{} : {}\n'.format(k, v))
        return r

    def add_ranking_info(self, element, better_element):
        """record a ranking relation between two elements
        """

        self.graph[element].add(better_element)

    def update_graph(self, element_list, rank):
        """Add ranking information to the graph"""
        ordered_elements = utils.reorder(element_list, rank)
        for i in list(range(len(ordered_elements)))[1:]:
            self.add_ranking_info(
                element=ordered_elements[i],
                better_element=ordered_elements[i - 1]
            )

    def size(self):
        return len(self.graph)

    def get_original_index(self, element_to_find):
        """get original index of a given element
        """

        for i, element in enumerate(self.element_list):
            if element == element_to_find:
                return i
        raise Exception('element not found')

    def get_top_nodes(self, up_to=5, ignore=[]):
        """list of nodes that have no better known alternative

        up_to : limit number of returned nodes
        ignore : list of elements that should be ignored. they cannot be chosen not count as a better alternative for other elements"""
        top = []
        for element, better_elements in self.graph.items():
            if element in ignore:
                continue
            if len(better_elements - set(ignore)) == 0:
                top.append(element)
            if len(top) == up_to:
                break
        return top

    def remove_node(self, node):
        """remove node as a key and all references of it as better node
        """

        del self.graph[node]
        for better_nodes in self.graph.values():
            better_nodes.discard(node)

    def rank_elements(self, version=0):
        if version == 0:
            return self.rank_elements_version_0()
        if version == 1:
            return self.rank_elements_version_1()

    def rank_elements_version_0(self):
        """main ranking function

        ----| algo
        get up to 5 element from the graph that have no better options
            - if there is only one such element, it's the best one of the set, we take it out from the graph and store it in the sorted list.
            - if there is more than one:
                - rank the elements
                - update the graph


        """
        rank = []
        while self.size() > 0:
            top_nodes = self.get_top_nodes()
            if len(top_nodes) == 1:
                better_element_in_graph = top_nodes[0]
                self.remove_node(better_element_in_graph)
                rank.append(self.get_original_index(better_element_in_graph))
            else:
                batch_rank = base_lib.rank_elements(top_nodes)
                self.update_graph(top_nodes, batch_rank)
        return rank

    def rank_elements_version_1(self):
        """main ranking function

        improvement on version 0
        we try to always use the base ranking function on 5 elements
        when the list of nodes to rank is between 2 and 4, we add more nodes to rank. We add nodes that would be top nodes if the current top nodes werent top nodes.
        """
        # import pdb
        # pdb.set_trace()
        rank = []
        while self.size() > 0:
            top_nodes = self.get_top_nodes()
            if len(top_nodes) == 1:
                better_element_in_graph = top_nodes[0]
                self.remove_node(better_element_in_graph)
                rank.append(self.get_original_index(better_element_in_graph))
            else:
                to_rank = top_nodes
                while len(to_rank) < 5 and self.size() != len(to_rank):
                    to_rank.extend(self.get_top_nodes(
                        up_to=(5 - len(to_rank)),
                        ignore=to_rank))
                batch_rank = base_lib.rank_elements(to_rank)
                self.update_graph(to_rank, batch_rank)
        return rank
