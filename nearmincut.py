# -*- coding: utf-8 -*

"""
Extending max flow / min cut networkx implementation to solve the all near min cuts
problem (ANMCP) based on the B&W algorithm:

Balcioglu, A. and Wood, K. Network Interdiction & Stochasitc Integer Programming;
Kluwer Academic Publishers: Boston, 2003; pp 21-49. 
"""

import networkx as nx
from copy import deepcopy

def get_edges_between_partitions(G_orig,partition):                           
    """                                                                     
    Given two sets of nodes find all edges that connect the two components  
    """                                                                     
                                                                                
    edges_that_were_cut=[]
    for s in partition[0]:
        for t in partition[1]: 
            if((s,t) in G_orig.edges()): 
                edges_that_were_cut.append((s,t)) 
                              
    return edges_that_were_cut 
        

def enumerate_cuts(G_orig, G, s, t, e_incl, e_excl, near_min_weight, quasi_excl,
                    all_min_cuts, undirected_bool, max_num_cuts=None):
    """                                                                         
    Recursive algorithm to enumerate all near min cuts 
    
    Recursively constrains the possible solution of the min s-t cut of a graph
    by quasi-including and quasi-excluding all edges of the parent cutset    
    """                                                                         
    # return if we reach the max number of cuts                                 
    if(max_num_cuts is not None): 
        if(len(all_min_cuts)>=max_num_cuts): 
            return 
                                                                                    
    Gp=deepcopy(G) 


    # change the capacity of exclusion edges to quasi_excl
    for edge in e_excl:
        Gp.edge[edge[0]][edge[1]]['capacity']=quasi_excl
        # if the graph was originally undirected, we need to remember we
        # have artifically placed two anti-directed parallel edges that both
        # need to be modified in the same ways
        if(undirected_bool):
            Gp.edge[edge[1]][edge[0]]['capacity']=quasi_excl
        
    # add artificial edges with capacity of quasi_excl 
    # to force inclusion of the inclusion edges           
    for (u,v) in e_incl: 
        # add artificial edge from s to u 
        Gp.add_edge(s, u) 
        Gp.edge[s][u]['capacity']=quasi_excl
        if(undirected_bool):
            Gp.add_edge(u, s)
            Gp.edge[u][s]['capacity']=quasi_excl
                                                                                    
        # add artificial edge from v to t 
        Gp.add_edge(v, t) 
        Gp.edge[v][t]['capacity']=quasi_excl
        if(undirected_bool):
            Gp.add_edge(t, v) 
            Gp.edge[t][v]['capacity']=quasi_excl

    print("Iter")
    for edge in Gp.edges(data=True):
        print(edge)

    # compute new max-flow/min-cut (bc we need to ensure we have actually   
    # generated a new min cut after forcing edge inclusion/exclusion            
    cut_value, partition = nx.minimum_cut(                                      
        Gp, s, t, flow_func=nx.algorithms.flow.shortest_augmenting_path)    

    # get the cutset
    Cp = set(get_edges_between_partitions(G_orig, partition))
    print(cut_value, Cp)

    # stopping criteria  
    # return if non near minimal cut 
    if(cut_value > near_min_weight): 
        return 

    # ensure that despite the adding of the artificial edges, the proposed cut
    # is indeed still minimal in the original graph  
    tmp_weight=sum([G_orig.edge[edge[0]][edge[1]]['capacity'] for edge in Cp]) 
    if(tmp_weight<=near_min_weight):
        all_min_cuts.append((tmp_weight,Cp)) 

    # Modify the most recently identified cutset with the new excluded/included edges
    for edge in Cp - e_incl: 
        edge=set([(edge[0],edge[1])]) 

        e_excl = e_excl.union(edge) 

        enumerate_cuts(G_orig, G, s, t, e_incl, e_excl, near_min_weight, 
                        quasi_excl, all_min_cuts, max_num_cuts)

        e_excl = e_excl - edge 

        e_incl = e_incl.union(edge) 

    return 


def near_min_cuts(G, s, t, max_out_cuts=None, **kwargs):

    """Use the recursive search of Balgioglu and Wood to enumerate all
       near_min_cuts

    Parameters
    ----------
    G : NetworkX graph
        Edges of the graph are expected to have an attribute called
        'capacity'. If this attribute is not present, the edge is
        considered to have infinite capacity.
            - If G is a directed graph, nothing further done
            - If G is an undirected graph, it is converted to a directed graph
              by replacing each undirected edge with two anti-directed parallel
              edges, both with equal capacity to the original undirected edge

    s : node
        Source node for the flow.

    t : node
        Sink node for the flow.



    max_out_cuts : terminates the recursive algorithm after finding this
                   number of near min cuts. It's important to give the algorithm
                   an escape since the size of the recursion tree is
                   exponential in the cardinality of (# of edges in) the min cut 

    **kwargs : 
    
        None: eps = 0

        eps : will return any cut between s and t whose capacity is 
              <=(1+eps)*C0 where C0 is the total cut capacity of the min cut

        eps_k : overrides eps if specified
                Will return any cut between s and t whose capacity is
                <=C0+eps_k


    Returns
    -------

    List of tuples [(cut_value, cutset)] : list of all near-min cuts

    cut_value : float
        Value of a near minimal cut, i.e., sum of the capacities of the edges
        that were cut

    cutset : set of 2-tuples
        A set of edges that were cut

    Raises
    ------
    ValueError
        An argument other than eps or eps_k was passed to kwargs

    NetworkXError
        The algorithm does not support MultiGraph and MultiDiGraph. If
        the input graph is an instance of one of these two classes, a
        NetworkXError is raised.

    NetworkXUnbounded
        If the graph has a path of infinite capacity, the value of a
        feasible flow on the graph is unbounded above and the function
        raises a NetworkXUnbounded.


    return all_near_min_cuts
    """

    # first convert to DiGraph if undirected but remember if it was undirected
    undirected_bool=False
    if(not nx.is_directed(G)):
        undirected_bool=True
        G=G.to_directed()

    # second, find the value of the min_cut
    cut_value, partition = nx.minimum_cut(                                      
        G, s, t, flow_func=nx.algorithms.flow.shortest_augmenting_path)    

    keys=kwargs.keys()
    if(len(keys) != 0):
        if('eps' in keys and 'eps_k' not in keys):
            near_min_weight=cut_value*(1+kwargs['eps'])
        elif('eps_k' in keys and 'eps' not in keys):
            near_min_weight=cut_value+kwargs['eps_k']
        else:
            raise ValueError("Can only specify either 'eps' or 'eps_k' in kwargs")
    else:
        near_min_weight = cut_value
  
    # compute value to assign to the capacity of excluded edges
    quasi_excl=near_min_weight*10000000
 
    # all near_min_cuts is each minimal or near minimal cut as defined by eps 
    all_near_min_cuts=[]
    enumerate_cuts(G, G, s, t, set(), set(), near_min_weight, quasi_excl,
                    all_near_min_cuts, undirected_bool, max_num_cuts=None)

    
    # sort cuts on cut_value
    all_near_min_cuts=sorted(all_near_min_cuts, key=lambda tup: tup[0])
    

    return all_near_min_cuts
