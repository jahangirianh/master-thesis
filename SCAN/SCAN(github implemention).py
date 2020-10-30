# -*- coding: utf-8 -*-

"""
SCAN: A Structural Clustering Algorithm for Networks
As described in http://ualr.edu/nxyuruk/publications/kdd07.pdf
"""

from collections import deque
import numpy as np
from scipy.sparse import csr_matrix
import networkx as nx 
import scipy as sp

def struct_similarity(vcols, wcols):
    """ Compute the similartiy normalized on geometric mean of vertices"""
    # count the similar rows for unioning edges
    count = [index for index in wcols if (index in vcols)]
    # geomean
    #need to account for vertex itself, add 2(1 for each vertex)
    ans = (len(count) +2) / (((vcols.size+1)*(wcols.size+1)) ** .5)
    return ans

def neighborhood(G, vertex_v, eps):
    """ Returns the neighbors, as well as all the connected vertices """
    N = deque()
    
    vcols = vertex_v.tocoo().col
    #print vertex_v
    #print vcols
    #check the similarity for each connected vertex
    for index in vcols:
        wcols = G[index,:].tocoo().col
        if struct_similarity(vcols, wcols)> eps:
            N.append(index)
    return N, vcols

def scan(G, eps =0.7, mu=4):
    """
    Vertex Structure = sum of row + itself(1)
    Structural Similarity is the geometric mean of the 2Vertex size of structure
    """
    
    c = 0
    v = G.shape[0]
    # All vertices are labeled as unclassified(-1)
    vertex_labels = -np.ones(v)
    # start with a neg core(every new core we incr by 1)
    cluster_id = -1
    for vertex in xrange(v):
        N ,vcols = neighborhood(G, G[vertex,:],eps)
        # must include vertex itself
        N.appendleft(vertex)
        if len(N) >= mu:
            #print(vertex)
            #print "we have a cluster at: %d ,with length %d " % (vertex, len(N))
            # gen a new cluster id (0 indexed)
            cluster_id +=1
            print "---------"
            print(cluster_id)
            
            print vertex
            # if vertex_labels[vertex] == -1:
            # print(vertex_labels)
            while N:
                 y = N.pop()
                 print ("y = ",y)
                 R , ycols = neighborhood(G, G[y,:], eps)
                 # include itself
                 R.appendleft(y)
                 print 'r=',R
                 # (struct reachable) check core and if y is connected to vertex
                 if len(R) >= mu:
                     print 'r = ',R
                     #print "we have a structure Reachable at: %d ,with length %d " % (y, len(R))
                     #print R
                     #print y
                     #print '------'
                     while R:
                         r = R.pop()
                         label = vertex_labels[r]
                         # if unclassified or non-member
                         if (label == -1) or (label==-5): 
                             vertex_labels[r] =  cluster_id
                         # unclassified ??
                         if label == -1:
                             #print r
                             N.appendleft(r)
                     print vertex_labels
        else:
            if vertex_labels[vertex] == -1:
                vertex_labels[vertex] = -5
        #print vertex_labels
    #classify non-members
    for index in np.where(vertex_labels ==-5)[0]:
        print "~~~~~~~~"
        print index
        ncols= G[index,:].tocoo().col
        if len(ncols) >=2:
            ## mark as a hub
            #print vertex_labels[index]
            vertex_labels[index] = -2 
            continue
            
        else:
            ## mark as outlier
            vertex_labels[index] = -3
            continue

    return vertex_labels

if __name__=='__main__':

    # Based on Example from paper
    rows = [0,0,0,0,1,1,1,2,2,2,3,3,3,3,4,4,4,4,
            5,5,5,5,5,6,6,6,6,6,6,7,7,7,7,8,8,8,
            9,9,9,9,10,10,10,10,11,11,11,11,
            12,12,12,12,12,13]
    cols = [1,4,5,6,0,5,2,1,5,3,2,4,5,6,0,3,5,6,
            0,1,2,3,4,4,0,3,7,11,10,6,11,12,8,7,
            12,9,8,12,10,13,9,12,11,6,7,12,10,6,
            7,8,9,10,11,9]
    data = np.ones(len(rows))
    # G =csr_matrix((data,(rows,cols)),shape=(14,14))

    G_amazon = nx.read_edgelist("data/amazon0312.txt", create_using=nx.Graph(), nodetype=int)
    A = nx.to_scipy_sparse_matrix(G_amazon)
    # G =csr_matrix(G_amazon,shape=(14,14))
    #print G.todense()
    #print neighborhood(G, G[0,:],.4 )
    print scan(A, 0.7, 4)
    %time