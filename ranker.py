import utils
import base_lib
from graph import Graph
from copy import copy
from pdb import set_trace as bp


def rank_elements(element_list, version=0):
    if version == 0:
        return rank_elements_version_0(element_list)
    elif version == 1:
        return rank_elements_version_1(element_list)
    elif version == 2:
        return rank_elements_version_2(element_list)
    else:
        raise ValueError('unknown version : {}'.format(version))


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


def rank_elements_version_2(element_list):
    """main ranking function

    improvement on version 0
    We try to always use the base ranking function on 5 elements
    When the list of nodes to rank is between 2 and 4, we add more
     nodes to rank from the direct sucessors of the top nodes.
    """
    graph = Graph(element_list)
    rank = []
    while graph.size() > 0:
        print()
        print('graph size : {}'.format(graph.size()))
        # bp()
        # if len(graph.get_top_nodes()) == 0:
        #     bp()
        top_nodes = graph.get_top_nodes()

        print('top nodes : {}'.format(len(top_nodes)))
        if len(top_nodes) == 1:
            print('>>popping element')
            better_element_in_graph = top_nodes[0]
            original_index = graph.remove_node(better_element_in_graph)
            rank.append(original_index)
        else:
            to_rank = [top_nodes]  # lists of nodes, and their sucessors
            # conditions to keep adding nodes to the ranking batch:
            # there is less than 5 nodes to compare
            while sum([len(level) for level in to_rank]) \
                    < min(5, graph.size()):
                # optimization : we add sucessor of top nodes to the list of
                # nodes to rank until we have at least 5 nodes. We can do
                # various rounds of it.
                next_level = []  # sucessors of the last added nodes
                for node in to_rank[-1]:
                    sucessors = graph.get_direct_lower_nodes(node)
                    next_level.extend(sucessors)
                to_rank.append(next_level)
                if len(to_rank[-1]) == 0:
                    break  # if we cant add more nodes, stop the loop
                print('add {} more nodes to rank'.format(len(to_rank[-1])))
            to_rank = utils.reduce_list(to_rank)
            # limit to 5 elements
            to_rank = to_rank[:min(5, len(to_rank))]
            print('ranking {}'.format(len(to_rank)))
            batch_rank = base_lib.rank_elements(to_rank)
            graph.update_graph(to_rank, batch_rank)
    return rank
