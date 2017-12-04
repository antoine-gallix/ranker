import base_lib
import utils
from graph import Graph
import pytest


@pytest.fixture
def g():
    return Graph(utils.create_element_set(10))


class Elements_Generator():

    def __init__(self):
        self.i = 0

    def get_one(self):
        e = base_lib.Element(self.i)
        self.i += 1
        return e

    def get(self, n):
        es = []
        for _ in range(n):
            es.append(self.get_one())
        return es


@pytest.fixture
def eg():
    return Elements_Generator()


def test_graph_creation(eg):
    empty = Graph([])
    assert empty.size() == 0
    g = Graph(eg.get(10))
    assert g.size() == 10


def test_graph_creation_no_repeated_nodes(eg):
    A = eg.get_one()
    B = A
    g = Graph([A, B])
    assert g.size() == 1


def test_get_nodes(g):
    n = g.get_nodes(3)
    assert len(n) == 3


def test_add_edge(g):
    A, B = g.get_nodes(2)
    g.add_edge(A, B)


def test_add_edge_no_repetition(g):
    A, B = g.get_nodes(2)
    g.add_edge(A, B)
    g.add_edge(A, B)
    assert g.edge_count() == 1


def test_is_top_node(g):
    A, B = g.get_nodes(2)
    g.add_edge(A, B)
    assert g.is_top_node(A)
    assert g.is_top_node(B) is False


def test_remove_node(g):
    A, B, C = g.get_nodes(3)
    g.add_edge(A, B)
    g.add_edge(C, A)
    assert A in g
    assert g.edge_count() == 2
    g.remove_node(A)
    assert A not in g
    assert g.edge_count() == 0


def test_get_top_end_nodes(eg):
    g = Graph(eg.get(4))
    A, B, C = g.get_nodes(3)

    top_nodes = g.get_top_nodes()
    assert len(top_nodes) == 4

    end_nodes = g.get_end_nodes()
    assert len(end_nodes) == 4

    g.add_edge(A, B)
    g.add_edge(B, C)

    top_nodes = g.get_top_nodes()
    assert len(top_nodes) == 2
    assert A in top_nodes
    assert B not in top_nodes
    assert C not in top_nodes

    end_nodes = g.get_end_nodes()
    assert len(end_nodes) == 2
    assert C in end_nodes
    assert A not in end_nodes
    assert B not in end_nodes


def test_get_low_high_nodes(g):
    High1, High2, Middle, Low1, Low2 = g.get_nodes(5)
    g.add_edge(High1, Middle)
    g.add_edge(High2, Middle)
    g.add_edge(Middle, Low1)
    g.add_edge(Middle, Low2)

    assert High1 in g.get_direct_higher_nodes(Middle)
    assert High2 in g.get_direct_higher_nodes(Middle)
    assert Low1 in g.get_direct_lower_nodes(Middle)
    assert Low2 in g.get_direct_lower_nodes(Middle)


def test_update_graph(g):
    A, B, C = g.get_nodes(3)
    g.update_graph([A, B, C], [0, 1, 2])
    assert A in g.get_direct_higher_nodes(B)
    assert B in g.get_direct_higher_nodes(C)
    assert g.edge_count() == 2


def test_get_original_index(eg):
    elements = eg.get(3)
    g = Graph(elements)
    random_element = g.get_nodes(1)
    index = g.remove_node(random_element)
    assert elements[index] == random_element
