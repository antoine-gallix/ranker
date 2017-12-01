import utils
import base_lib
import pytest


def test_create_element_set():
    element_set = utils.create_element_set(5)
    assert len(element_set) == 5
    assert isinstance(element_set[0], base_lib.Element)


def test_element_set_uniqueness():
    element_set = utils.create_element_set(5)
    ids = [t.value for t in element_set]
    assert len(set(ids)) == 5


def test_is_ranking_correct_base_assertion():
    """test the ranking passes basic validation"""
    element_set = utils.create_element_set(4)
    long_rank = [2, 1, 0, 3, 4]
    not_a_rank = [2, 1, 0, 8]
    with pytest.raises(ValueError):
        assert utils.is_ranking_correct(element_set, long_rank)
    with pytest.raises(ValueError):
        assert utils.is_ranking_correct(element_set, not_a_rank)


def test_is_ranking_correct():
    """test the ranking is correct"""
    element_set = [
        base_lib.Element(3),
        base_lib.Element(5),
        base_lib.Element(6),
        base_lib.Element(0),
    ]
    good_rank = [2, 1, 0, 3]
    bad_rank = [0, 1, 2, 3]
    assert utils.is_ranking_correct(element_set, bad_rank) is False
    assert utils.is_ranking_correct(element_set, good_rank)


def test_reorder():
    seq = ['b', 'c', 'a']
    assert utils.reorder(seq, [2, 0, 1]) == ['a', 'b', 'c']
