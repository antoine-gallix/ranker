class Element:
    """The object we want to rank

    It simply has a value.
    """

    def __init__(self,
                 value):
        self.value = value

    def __repr__(self):
        return '<Element({})>'.format(self.value)


def rank_elements(elements):
    """Return the index of the elements in DECREASING ranking order.

    ex :
    # if e2 > e1 > e3
    >>>rank=rank_trip([e1,e2,e3])
    >>>rank
    [1,0,2]
    # better ranked element:
    >>>rank[0]
    e2
    # less ranked element:
    >>>rank[-1]
    e3

    This function simply ranks elements by their 
    """
    if len(elements) > 5:
        raise ValueError(
            'No more than 5 elements can be ranked at the same time')

    indexed_element_list = list(zip(range(len(elements)), elements))
    indexed_element_list.sort(key=lambda x: x[1].value, reverse=True)
    return [indexed_element[0] for indexed_element in indexed_element_list]
