import utils
import base_lib
from graph import Graph


def rank_elements(element_list, version=0):
    if version == 0:
        return rank_elements_version_0(element_list)
    elif version == 1:
        return rank_elements_version_1(element_list)


def rank_elements_version_0(element_list):
    """main ranking function

    ----| algo
    get up to 5 element from the graph that have no better options
        - if there is only one such element, it's the best one of the set, we take it out from the graph and store it in the sorted list.
        - if there is more than one:
            - rank the elements
            - update the graph
    """
    graph = Graph(element_list)
    rank = []
    while graph.size() > 0:
        top_nodes = graph.get_top_nodes()
        if len(top_nodes) == 1:
            better_element_in_graph = top_nodes[0]
            original_index = graph.remove_node(better_element_in_graph)
            rank.append(original_index)
        else:
            # limit to 5 elements
            top_nodes = top_nodes[:min(5, len(top_nodes))]
            batch_rank = base_lib.rank_elements(top_nodes)
            graph.update_graph(top_nodes, batch_rank)
    return rank


def rank_elements_version_1(element_list):
    """main ranking function

    improvement on version 0
    We now can also rank lowest nodes and pull the lowest elements from the graph.
    """
    graph = Graph(element_list)
    top_rank = []
    low_rank = []
    while graph.size() > 0:
        top_nodes = graph.get_top_nodes()
        end_nodes = graph.get_end_nodes()
        # Pull sorted elements first if possible
        if len(top_nodes) == 1:
            better_element_in_graph = top_nodes[0]
            original_index = graph.remove_node(better_element_in_graph)
            top_rank.append(original_index)
        elif len(end_nodes) == 1:
            worst_element_in_graph = end_nodes[0]
            original_index = graph.remove_node(worst_element_in_graph)
            low_rank.append(original_index)
        # Rank top or end nodes, depending of which has more nodes available
        else:
            if len(top_nodes) >= len(end_nodes):
                to_rank = top_nodes
            else:
                to_rank = end_nodes
            # limit to 5 elements
            to_rank = to_rank[:min(5, len(to_rank))]
            batch_rank = base_lib.rank_elements(to_rank)
            graph.update_graph(to_rank, batch_rank)
    # merge high and low rankings
    rank = top_rank + low_rank[::-1]
    return rank


def rank_elements_version_2(self):
    """main ranking function

    improvement on version 0
    we try to always use the base ranking function on 5 elements
    when the list of nodes to rank is between 2 and 4, we add more nodes to rank. We add nodes that would be top nodes if the current top nodes werent top nodes.
    """
    rank = []
    while self.graph.size() > 0:
        top_nodes = self.graph.get_top_nodes()
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
