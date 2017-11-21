# -*- coding: utf-8 -* 

import nearmincut as nmc
import networkx as nx


graph_representation="""

G = nx.DiGraph()
>>>G.add_edge('x','a', capacity=3.0)
>>>G.add_edge('x','b', capacity=1.0)
>>>G.add_edge('a','c', capacity=3.0)
>>>G.add_edge('b','c', capacity=5.0)
>>>G.add_edge('b','d', capacity=4.0)
>>>G.add_edge('d','e', capacity=2.0)
>>>G.add_edge('c','y', capacity=2.0)
>>>G.add_edge('e','y', capacity=3.0)

>>>kwargs={'eps':5}
>>>nmc.near_min_cuts(G,'x','y',**kwargs)
"""
print("Graph representation:")
print(graph_representation)

# Simple directed graph
kwargs={'eps':5}
G = nx.DiGraph()
G.add_edge('x','a', capacity=3.0)
G.add_edge('x','b', capacity=1.0)
G.add_edge('a','c', capacity=3.0)
G.add_edge('b','c', capacity=5.0)
G.add_edge('b','d', capacity=4.0)
G.add_edge('d','e', capacity=2.0)
G.add_edge('c','y', capacity=2.0)
G.add_edge('e','y', capacity=3.0)

sol=nmc.near_min_cuts(G,'x','y',**kwargs)

print("Solution0 for eps=5 on directed graph:")
for elem in sol: 
    print(elem)


# The same graph as above, but when there is an anti-parallel edge
# (for each forward edge) with the same weight
G1 = nx.DiGraph()
G1.add_edge('x','a', capacity=3.0)
G1.add_edge('a','x', capacity=3.0)
G1.add_edge('x','b', capacity=1.0)
G1.add_edge('b','x', capacity=1.0)
G1.add_edge('a','c', capacity=3.0)
G1.add_edge('c','a', capacity=3.0)
G1.add_edge('b','c', capacity=5.0)
G1.add_edge('c','b', capacity=5.0)
G1.add_edge('b','d', capacity=4.0)
G1.add_edge('d','b', capacity=4.0)
G1.add_edge('d','e', capacity=2.0)
G1.add_edge('e','d', capacity=2.0)
G1.add_edge('c','y', capacity=2.0)
G1.add_edge('y','c', capacity=2.0)
G1.add_edge('e','y', capacity=3.0)
G1.add_edge('y','e', capacity=3.0)

sol1=nmc.near_min_cuts(G1,'x','y',**kwargs)

print("\nSolution1 for eps=5 on same directed graph but with antiparallel edges added:")
print("(NOTE, NOT EQUAL to Solution0)")
for elem in sol1: 
    print(elem)


# Same graph but undirected 
G2 = nx.Graph()
G2.add_edge('x','a', capacity=3.0)
G2.add_edge('x','b', capacity=1.0)
G2.add_edge('a','c', capacity=3.0)
G2.add_edge('b','c', capacity=5.0)
G2.add_edge('b','d', capacity=4.0)
G2.add_edge('d','e', capacity=2.0)
G2.add_edge('c','y', capacity=2.0)
G2.add_edge('e','y', capacity=3.0)

sol=nmc.near_min_cuts(G2,'x','y',**kwargs)

print("\nSolution2 for eps=5 on undirected graph:")
print("(NOTE, EQUAL to Solution1)")
for elem in sol: 
    print(elem)
