# ranker
Training project. Make an unlimited ranking function out of a limited base ranking function.

## Problem statement

It's a ranking problem.

We first create a base library that expose an Element class that has an internal value, and a base ranking function that can rank a set of maximum 5 elements. The base ranking function is the only one that is allow to access the internal value of the Elements and rank them according to it.

We want to create a ranking function that can rank an arbitrary number of Elements. The ranking conputation from the base function is supposed to be a costly operation that we want to minimize the use of, but it's cost is independant of the number of Elements ranked, as long as the number of Elements is not higher that 5.

## Modeling information

Each time we use the base ranking function on a batch of Elements, which size is of 5 maximum, we gather ranking information on our global set of Elements. As we keep accumulating information, we eventualy reach a point where we can rank the whole set of Elements.

We represent our set as a directed graph, where the nodes are Elements and the directed edges represent the ranking information. Each time we use the base ranking function, we can add up to 5 new edges to the graph.

    E1,E2,E3,E4,E5 =ranking=> E2>E3>E4>E1>E5

The graph is fully ranked when each node can be related to every other nodes in the graph following edges in one direction.

## Solutions

### Brute force

A simple brute force algorithm would be to add edges until this condition is met. The problem is that depending of the state of the graph, not all edges add information. If we know that E1>E2>E3, evaluating the edge between E1 and E3 adds no information. We then need to choose batches of nodes that has no known information between them.

### Sort out the best first

A simple strategy to choose nodes is to rank against each other nodes that have no better known alternative, we call them top nodes, and repeat until only one is left, which will be the higher ranked node. We can remove it from the graph and repeat the process. This idea is implemented in version 0 of the ranking function.

    VERSION 0
    initialize the graph nodes with the given trip set
    until the graph is empty:
        get up to 5 trip from the graph that have no better options
            - if there is only one such trip, it's the best one of the set, we take it out from the graph and store it in the sorted list.
            - if there is more than one:
                - rank the trips
                - update the graph

### Best or worst

The problem with the previous strategy is that after the first phase where we rank mostly single nodes, we reach a point where the graph is fully connected and the number of top nodes remaining in the graph after removing the better node of all at each step is low, and we wont make the best use of our base ranking function calling it with fewer than 5 elements. But if we start to choose top nodes, by definition, their relation with all nodes below them is already known and it's therefore useless to add one of those lower nodes to the next batch to rank.

A first modification of the algorithm would be, if the number of top node is inferior to 5, to start the process in the other direction and start ranking against each other nodes that have no worst node known, that we can call end nodes. We now can start taking out nodes from the graph from the two sides, the best and the worst. We choose the side that offer the most nodes.

    VERSION 1
    initialize the graph nodes with the given trip set
    until the graph is empty:
        How many nodes have no better alternative (top nodes)?
        How many nodes have no worse alternative (end nodes)?
        Get up to 5 trip from the options that has more nodes
            - if there is only one such trip, it's the best one of the set, we take it out from the graph and store it in the sorted list.
            - if there is more than one:
                - rank the trips
                - update the graph

### Unrelated nodes in the middle

In the case of neither top or end nodes are enough to form a full batch of 5, we could then explore methods to find unrelated nodes from the middle of the chains.

## requirements

pytest

## installation

- start a virtual environement (python 3)
- install requirements:
    
    pip install pytest

- run unit tests
    py.test
- run manual internal tests
    python scratch_unit.py
- run manual final test
    python scratch.py