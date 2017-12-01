"""Test the ranker function
"""
import utils
import ranker
import base_lib

# ----| ranker_graph internals


def test_graph_creation():
    """graph creation, internal graph and element list length
    """
    elements = utils.create_element_set(10)
    g = ranker.ranker_graph(elements)
    assert len(g.graph) == 10
    assert len(g.element_list) == 10


def test_add_ranking_info():
    """ranker_graph.add_ranking_info()"""
    element_A = base_lib.Element(1)
    element_B = base_lib.Element(2)
    g = ranker.ranker_graph([element_A, element_B])
    g.add_ranking_info(element_A, element_B)
    assert element_B in g.graph[element_A]
    assert (element_A in g.graph[element_B]) is False


def test_update_graph():
    """ranker_graph.update_graph()"""
    element_A = base_lib.Element(1)
    element_B = base_lib.Element(2)
    element_C = base_lib.Element(3)
    g = ranker.ranker_graph([element_A, element_B, element_C])
    g.update_graph([element_A, element_B, element_C], [0, 1, 2])
    assert g.graph[element_A] == set()
    assert g.graph[element_B] == set([element_A])
    assert g.graph[element_C] == set([element_B])


def test_get_original_index():
    """ranker_graph.get_original_index()"""
    elements = utils.create_element_set(10)
    g = ranker.ranker_graph(elements)
    assert g.get_original_index(elements[0]) == 0
    assert g.get_original_index(elements[5]) == 5


def test_size():
    """ranker_graph.size()"""
    g = ranker.ranker_graph([])
    assert g.size() == 0
    elements = utils.create_element_set(10)
    g = ranker.ranker_graph(elements)
    assert g.size() == 10


def test_get_top_nodes():
    """ranker_graph.get_top_nodes()"""
    element_A = base_lib.Element(1)
    element_B = base_lib.Element(2)
    element_C = base_lib.Element(3)
    g = ranker.ranker_graph([element_A, element_B, element_C])
    g.update_graph([element_A, element_B], [0, 1])
    top_nodes = g.get_top_nodes()
    assert len(top_nodes) == 2
    assert set(top_nodes) == set([element_A, element_C])


def test_get_top_nodes_ignore():
    """ranker_graph.get_top_nodes()"""
    elements = utils.create_element_set(15)
    g = ranker.ranker_graph(elements)
    print(g)
    top = g.get_top_nodes()
    print(top)
    next_top = g.get_top_nodes(ignore=top)
    print(next_top)
    assert set(top) & set(next_top) == set()


def test_remove_node():
    """ranker_graph.remove_node()"""
    elements = utils.create_element_set(10)
    g = ranker.ranker_graph(elements)
    to_remove = elements[5]
    g.update_graph([to_remove, elements[6], elements[7]], [0, 1, 2])
    g.update_graph([elements[8], to_remove, elements[9]], [0, 1, 2])
    # before removal
    assert to_remove in g.graph.keys()
    assert to_remove in g.graph[elements[6]]
    assert to_remove in g.graph[elements[9]]

    g.remove_node(to_remove)

    # after removal
    assert to_remove not in g.graph.keys()
    for superior_nodes in g.graph.values():
        assert to_remove not in superior_nodes

# ----| ranker_graph main ranking function


def test_ranker_version_0():
    elements = utils.create_element_set(1000)
    rank = ranker.rank_elements(elements)
    assert utils.is_ranking_correct(elements, rank)


def test_ranker_version_1():
    elements = utils.create_element_set(1000)
    rank = ranker.rank_elements(elements, version=1)
    assert utils.is_ranking_correct(elements, rank)
