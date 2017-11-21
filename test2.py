# -*- coding: utf-8 -* 

import nearmincut as nmc
import networkx as nx


graph_representation=\
""">>>G=nx.DiGraph()
>>>G.add_edge('s','1', capacity=5.0)
>>>G.add_edge('s','2', capacity=5.0)
>>>G.add_edge('1','3', capacity=2.0)
>>>G.add_edge('1','6', capacity=1.0)
>>>G.add_edge('2','4', capacity=2.0)
>>>G.add_edge('2','5', capacity=4.0)
>>>G.add_edge('3','4', capacity=7.0)
>>>G.add_edge('3','t', capacity=8.0)
>>>G.add_edge('4','5', capacity=1.0)
>>>G.add_edge('5','7', capacity=3.0)
>>>G.add_edge('6','t', capacity=4.0)
>>>G.add_edge('7','t', capacity=7.0)

>>>nmc.near_min_cuts(G,'x','y',**kwargs)
"""
print("Graph representation:")
print(graph_representation)

###########################
# Simple directed graph

#kwargs={'eps':0.125}
kwarg='eps_k'
kwargs={kwarg:2}
G = nx.DiGraph()
G.add_edge('s','1', capacity=5.0)
G.add_edge('s','2', capacity=5.0)
G.add_edge('1','3', capacity=2.0)
G.add_edge('1','6', capacity=1.0)
G.add_edge('2','4', capacity=2.0)
G.add_edge('2','5', capacity=4.0)
G.add_edge('3','4', capacity=7.0)
G.add_edge('3','t', capacity=8.0)
G.add_edge('4','5', capacity=1.0)
G.add_edge('5','7', capacity=3.0)
G.add_edge('6','t', capacity=4.0)
G.add_edge('7','t', capacity=7.0)

sol=nmc.near_min_cuts(G,'s','t',**kwargs)

print("Solution0 for %s=%s on directed graph:"%(kwarg,str(kwargs['eps_k'])))
for elem in sol: 
    print(elem)


###########################
# The same graph as above, but when there is an anti-parallel edge
# (for each forward edge) with the same weight

kwargs={'eps':0.125}
G1 = nx.DiGraph()
G1.add_edge('s','1', capacity=5.0)
G1.add_edge('1','s', capacity=5.0)
G1.add_edge('s','2', capacity=5.0)
G1.add_edge('2','s', capacity=5.0)
G1.add_edge('1','3', capacity=2.0)
G1.add_edge('3','1', capacity=2.0)
G1.add_edge('1','6', capacity=1.0)
G1.add_edge('6','1', capacity=1.0)
G1.add_edge('2','4', capacity=2.0)
G1.add_edge('4','2', capacity=2.0)
G1.add_edge('2','5', capacity=4.0)
G1.add_edge('5','2', capacity=4.0)
G1.add_edge('3','4', capacity=7.0)
G1.add_edge('4','3', capacity=7.0)
G1.add_edge('3','t', capacity=8.0)
G1.add_edge('t','3', capacity=8.0)
G1.add_edge('4','5', capacity=1.0)
G1.add_edge('5','4', capacity=1.0)
G1.add_edge('5','7', capacity=3.0)
G1.add_edge('7','5', capacity=3.0)
G1.add_edge('6','t', capacity=4.0)
G1.add_edge('t','6', capacity=4.0)
G1.add_edge('7','t', capacity=7.0)
G1.add_edge('t','7', capacity=7.0)

sol1=nmc.near_min_cuts(G1,'s','t',**kwargs)

print("\nSolution1 for eps=%s on same directed graph but with antiparallel edges added:"%str(kwargs['eps']))
print("(NOTE, NOT EQUAL to Solution0)")
for elem in sol1: 
    print(elem)


###########################
# Same graph but undirected 

G2 = nx.Graph()
G2.add_edge('s','1', capacity=5.0)
G2.add_edge('s','2', capacity=5.0)
G2.add_edge('1','3', capacity=2.0)
G2.add_edge('1','6', capacity=1.0)
G2.add_edge('2','4', capacity=2.0)
G2.add_edge('2','5', capacity=4.0)
G2.add_edge('3','4', capacity=7.0)
G2.add_edge('3','t', capacity=8.0)
G2.add_edge('4','5', capacity=1.0)
G2.add_edge('5','7', capacity=3.0)
G2.add_edge('6','t', capacity=4.0)
G2.add_edge('7','t', capacity=7.0)

sol=nmc.near_min_cuts(G2,'s','t',**kwargs)

print("\nSolution2 for eps=%s on undirected graph:"%str(kwargs['eps']))
print("(NOTE, EQUAL to Solution1)")
for elem in sol: 
    print(elem)
