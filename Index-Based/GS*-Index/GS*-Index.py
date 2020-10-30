#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:


def read_graph(file):
    G = nx.read_edgelist(file, create_using=nx.Graph(), nodetype=int)
    print(nx.info(G))
#     sp_pos = nx.spring_layout(G)
#     plt.axis("off")
#     nx.draw_networkx(G, pos=sp_pos, with_labels=True, node_size=35)
    return G


# In[ ]:


def structural_similarities(G):
    """

    """
    ss = {}
    for edge in G.edges:
        node1 = edge[0]
        node2 = edge[1]
        c_neighbours = len(list(nx.common_neighbors(G, node1, node2))) + 2

        n1_neighbours = len(G[node1]) + 1
        n2_neighbours = len(G[node2]) + 1
        # print(c_neighbours)

        edge_ss = c_neighbours / ((n1_neighbours * n2_neighbours) ** 0.5)
        ss[edge] = edge_ss
    return ss


# In[4]:


def neighbours(G, node):
    en = set()
#     en.add(node)
    for neighbour in G.neighbors(node):
        en.add(neighbour)
    return en


# In[5]:


def GSS_Construct(G):
    ss = structural_similarities(G)
    print('******************')
    NO = {}  # []
    max_deg = 0
    j = 0
    for node in G.nodes:
        NO_node = {}
        NO_node[node] = 1
        ne = neighbours(G, node)
        if(len(ne) > max_deg):
            max_deg = len(ne) + 1
        for i in ne:
            if (node, i) in ss:
                NO_node[i] = ss[(node, i)]
            else:
                NO_node[i] = ss[(i, node)]

        NO_node = {k: v for k, v in sorted(
            NO_node.items(), key=lambda x: x[1], reverse=True)}

#         print(j)
#         j += 1
#         NO.append(NO_node)
        NO[node] = NO_node

    CO = []
    for mu in range(2, max_deg + 1):
        print(mu)
        CO_mu = {}
        for node in G.nodes:
            if(len(list(G.neighbors(node))) + 1 >= mu):
                CO_mu[node] = list(NO[node].items())[mu-1][1]
#         CO_mu = pot_cores(G, mu)
        CO_mu = {k: v for k, v in sorted(
            CO_mu.items(), key=lambda x: x[1], reverse=True)}

        CO.append(CO_mu)

#     CO
    return NO, CO


# In[ ]:
# G = DBLP
'''
ss = structural_similarities(G)
print('******************')
NO = {}
max_deg = 0
j = 0
for node in G.nodes:
    NO_node = {}
    NO_node[node] = 1
    ne = neighbours(G, node)
    if(len(ne) > max_deg):
        max_deg = len(ne) + 1
    for i in ne:
        if (node, i) in ss:
            NO_node[i] = ss[(node, i)]
        else:
            NO_node[i] = ss[(i, node)]

    NO_node = {k: v for k, v in sorted(
        NO_node.items(), key=lambda x: x[1], reverse=True)}

#         print(j)
#         j += 1
    NO[node] = NO_node

'''
# In[ ]:


# NO[369692]


# In[ ]:

'''
CO = []
for mu in range(2, max_deg + 1):
    #     print(mu)
    CO_mu = {}
    for node in G.nodes:
        #         print(node)
        if(len(list(G.neighbors(node))) + 1 >= mu):
            CO_mu[node] = list(NO[node].items())[mu-1][1]
#         CO_mu = pot_cores(G, mu)
    CO_mu = {k: v for k, v in sorted(
        CO_mu.items(), key=lambda x: x[1], reverse=True)}

    CO.append(CO_mu)
'''

# In[6]:


def GSS_Query(G, NO, CO, mu, eps):
    Cluster = []
#     mu = 4
#     eps = 0.7
    nx.set_node_attributes(G, 'not', 'label')
    G_nodes = G.nodes
    for u in CO[mu-2]:
        if(G_nodes[u]['label'] == 'explored'):
            continue
    #     print('u',u)
        v = list(NO[u].items())[mu-1]
    #     print('v',v)
        if(v[1] < eps):
            break
        C = set()
        C.add(u)
        Q = set()
        Q.add(u)
        G_nodes[u]['label'] = 'explored'
        while(Q):
            #         print('  Q',Q)
            v = Q.pop()
    #         print('  v2',v)
            for w in NO[v]:
                #             print('    w',w)
                if(NO[v][w] < eps):
                    break
                if(G_nodes[w]['label'] == 'explored'):
                    continue
                G_nodes[w]['label'] = 'explored'
                C.add(w)

                #############     might be wrong     ################
                if(len(list(NO[w].items())) > mu - 1):
                    t = list(NO[w].items())[mu-1]
    #                 print('    t',t)
                    if(t[1] >= eps):
                        Q.add(w)
#                         print(w)
                    else:
                        G_nodes[w]['label'] = 'non-core'
    #                 print('    Q2',Q)
                else:
                    G_nodes[w]['label'] = 'non-core'

#                 if(t[1] >= eps):

        # print(nx.get_node_attributes(G, 'label'))
        Cluster.append(C)
#         print('Cluster', Cluster)

    return Cluster


# In[ ]:
G = read_graph("data/amazon0312.txt")


# In[ ]:


NO, CO = GSS_Construct(G)
print("NO", NO)
print("CO", CO)


# In[ ]:


GSS_Query(G, NO, CO, 5, 0.6)


# In[ ]:


GSS_Query(G, NO, CO, 4, 0.7)


# In[ ]:


nx.get_node_attributes(G, 'label')


# In[7]:


DBLP = read_graph("../../../DataSets/com-dblp.ungraph.txt")


# In[8]:


NO, CO = GSS_Construct(DBLP)


# In[ ]:


print(NO)


# In[ ]:


#GSS_Query(DBLP, NO, CO, 5, 0.6)


# In[ ]:
