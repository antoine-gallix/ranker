"""Test the ranker function
"""
import utils
import ranker
import pytest


@pytest.fixture
def set_dev():
    return utils.create_element_set(48)


@pytest.fixture
def set_1000():
    return utils.create_element_set(1000)

# ----| ranker_graph main ranking function


def test_ranker_version_0(set_1000):
    rank = ranker.rank_elements(set_1000, version=0)
    assert utils.is_ranking_correct(set_1000, rank)


def test_ranker_version_1(set_1000):
    rank = ranker.rank_elements(set_1000, version=1)
    assert utils.is_ranking_correct(set_1000, rank)


# def test_ranker_version_2_dev(set_dev):
#     rank = ranker.rank_elements(set_dev, version=2)
#     assert utils.is_ranking_correct(set_dev, rank)


# def test_ranker_version_2(set_1000):
#     rank = ranker.rank_elements(set_1000, version=2)
#     assert utils.is_ranking_correct(set_1000, rank)
