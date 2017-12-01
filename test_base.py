"""Test the base library
"""
import base_lib
import utils
import pytest
# ---------------------TESTS---------------------


def test_create_element():
    t = base_lib.Element(1000)
    assert t.value == 1000
    assert str(t) == '<Element(1000)>'


def test_rank_elements_no_more_than_5():
    """ranking accepts no more than 5 elements"""
    ts = utils.create_element_set(5)
    base_lib.rank_elements(ts)
    ts = utils.create_element_set(6)
    with pytest.raises(ValueError):
        base_lib.rank_elements(ts)


def test_rank_elements_is_valid_rank():
    """return value is a valid rank"""

    ts = utils.create_element_set(5)
    rank = base_lib.rank_elements(ts)
    rank.sort()
    assert rank == [0, 1, 2, 3, 4]


def test_rank_elements():
    """test base ranking function is correct"""

    unordered_element_set = [
        base_lib.Element(8),
        base_lib.Element(4),
        base_lib.Element(13),
        base_lib.Element(7),
    ]
    assert utils.is_ranking_correct(
        unordered_element_set, [0, 1, 2, 3]) is False

    rank = base_lib.rank_elements(unordered_element_set)
    assert utils.is_ranking_correct(unordered_element_set, rank)
