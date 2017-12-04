"""Test the ranker function
"""
import utils
import ranker

# ----| ranker_graph main ranking function


def test_ranker_version_0():
    elements = utils.create_element_set(1000)
    rank = ranker.rank_elements(elements)
    assert utils.is_ranking_correct(elements, rank)


def test_ranker_version_1():
    elements = utils.create_element_set(1000)
    rank = ranker.rank_elements(elements, version=1)
    assert utils.is_ranking_correct(elements, rank)
