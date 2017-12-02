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

### Best or worst

The problem with the previous strategy is that after the first phase where we rank mostly single nodes, we reach a point where the graph is fully connected and the number of top nodes remaining in the graph after removing the better node of all at each step is low, and we wont make the best use of our base ranking function calling it with fewer than 5 elements. But if we start to choose top nodes, by definition, their relation with all nodes below them is already known and it's therefore useless to add one of those lower nodes to the next batch to rank.

A first modification of the algorithm would be, if the number of top node is inferior to 5, to start the process in the other direction and start ranking against each other nodes that have no worst node known, that we can call end nodes. We now can start taking out nodes from the graph from the two sides, the best and the worst. We choose the side that offer the most nodes.

### Unrelated nodes in the middle

In the case of neither top or end nodes are enough to form a full batch of 5, we could then explore methods to find unrelated nodes from the middle of the chains.

## Graph implementation

To store this information we use a data structure, a dictionary, that holds for each trip of the set, the set of trips that we know are better ranked than it. At the end it's just like a simplified directed graph, where the nodes are trips and directed edges represent relation of ranking. We only store for each nodes, the direct predecessors in the graph.

For example :
We start to rank a set of 3 trips:
    
    ranking_graph={
        t1:[],
        t2:[],
        t3:[],
    }

We now update the graph after ranking the three trips (descending order, i.e. trips[rank[0]] is the best trip):

trips=[t1,t2,t3]
rank=rank_trips(trips)
update_ranking_graph(ranking_graph,trips,rank)

    ranking_graph={
        t1:[],
        t2:[t1],
        t3:[t2],
    }

We can then run the following algorithm:

initialize the graph with the given trip set
until the graph is empty:
    get up to 5 trip from the graph that have no better options
        - if there is only one such trip, it's the best one of the set, we take it out from the graph and store it in the sorted list.
        - if there is more than one:
            - rank the trips
            - update the graph

It's not yet an optimal algorithm but it will work.

----| optimization 1
If the ranking time of the base function is constant (assumption), independantly of the number of trip submitted, we should use the function at it's best, ensuring this base ranking function is always called on a list of 5 trips.
A possibility would be, when less than 5 trips have no better option known

----| optimization 2
To maximize the amount of information gained by calling the ranking function, we should ensure that the submitted trips have no ranking relation known yet, if possible. Which mean there is no chain of known ranking relation between the trips in our ranking graph.


---------------------requirements---------------------

pytest

---------------------installation---------------------

- start a virtual environement (python 3)
- install requirements:
    pip install pytest
- run unit tests
    py.test
- run manual internal tests
    python scratch_unit.py
- run manual final test
    python scratch.py