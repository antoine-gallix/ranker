import base_lib
import random
from copy import copy
from simple_profile import profile


def create_element_set(n):
    """Create a randomized set of n elements with unique values
    """
    element_set = [base_lib.Element(i) for i in range(n)]
    random.shuffle(element_set)
    return element_set


def is_ranking_correct(element_list, ranking):
    """Test if the ranking is correct"""

    if ranking is None:
        raise ValueError(
            'ranking is None')

    # same length
    if len(ranking) != len(element_list):
        raise ValueError(
            'given ranking has not the same length as element list')

    # a valid index of the element list
    ranking_ = copy(ranking)  # preserve original ranking from inplace sort
    ranking_.sort()
    if not ranking_ == list(range(len(ranking))):
        raise ValueError(
            'given ranking is not a valid indexer of the element list')

    # rank order the element list correctly
    values = [element.value for element in element_list]
    ids_from_rank = [values[i] for i in ranking]
    ids_sorted = copy(values)
    ids_sorted.sort(reverse=True)
    return ids_from_rank == ids_sorted


def reorder(sequence, index):
    """reorder a sequence from index"""
    return [sequence[i] for i in index]


def reduce_list(list_of_lists):
    """reduce a list of list into a list"""
    reduced = []
    for l in list_of_lists:
        reduced.extend(l)
    return reduced


def profile_ranker(ranking_function, set_size, repetitions):
    info = []
    base_lib.rank_elements = profile(base_lib.rank_elements)
    for _ in range(repetitions):
        print('.', end='', flush=True)
        base_lib.rank_elements.reset_profile()
        elements = create_element_set(set_size)
        rank = ranking_function(elements)
        assert is_ranking_correct(elements, rank)
        info.append({
            'set_size': set_size,
            'rank_call_count': base_lib.rank_elements.count_calls()
        })
    print()
    return info


# ----| printing

def title(s):
    print('\n------{}------\n'.format(s))
