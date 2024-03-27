# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:28:43 2022

@author: ipkov
"""

import numpy as np
import pandas as pd
import igraph as ig

import networkx as nx
from sklearn.manifold import trustworthiness
# see https://scikit-learn.org/stable/modules/generated/sklearn.manifold.trustworthiness.html




# data = pd.read_excel("./data/causal_data.xlsx", engine='openpyxl', index_col =0, sheet_name ="FPi_model")
# var_types = data.loc[:, 'Type']
# data.drop(labels = 'Type', axis = 1, inplace=True)
# rem_vars = data[data.isna().all(axis=1)].index
# data.drop(rem_vars, axis = 0, inplace=True)
# data.dropna(inplace=True, axis = 1)
# X = data.transpose()
# X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))

def DirectCorrelation(X, rem_vars, var_types):

    out_vars = []
    in_vars = []
    network_ids = {}

    G = nx.DiGraph()
    for j, i in enumerate(X.columns):
        #print(i)
        if var_types[i] == 'output':
                
                G.add_node(j)
                G.nodes[j]["type"] = "output"
                G.nodes[j]["id"] = i
                out_vars.append(i)
                network_ids[i] = j
                
        elif var_types[i] == 'input':
                rem = []
                if len(rem_vars) != 0:
                    for k in rem_vars:
                        rem.append(i == k)
                else:
                    rem = [False]

                if any(rem):
                    pass
                else:
                    in_vars.append(i) 
                    G.add_node(j)
                    G.nodes[j]["type"] = "input"
                    G.nodes[j]["id"] = i
                    network_ids[i] = j

    #%%
    # Should select what kind of correlation...
    for i in in_vars:
        for j in out_vars:
            in_data = 0
            if len(X.loc[:, i].shape): 
                in_data = X.loc[:, i].values.reshape(-1, 1) 
            else:
                in_data = X.loc[:, i]
            out_data = 0   
            if len(X.loc[:, j].shape): 
                out_data = X.loc[:, j].values.reshape(-1, 1) 
            else:
                out_data = X.loc[:, j] 
            
            w = trustworthiness(in_data, out_data, n_neighbors=3)  #np.corrcoef(in_data.transpose(), out_data.transpose()) 
            G.add_edge(network_ids[i], network_ids[j], weight = np.round(w, decimals = 4))
    
    #th = trustworthiness(X.loc[:, in_vars], X.loc[:, out_vars], n_neighbors=3)

    iG = ig.Graph.from_networkx(G)      

    colormap_dict = {'input' : '#00b4d9', 'output' : '#c70039', 'parameter' : '#ffc300', 'variable' : '#09ad03', 'computationnal' : '#BFBFBF' }
    colormap = []
    labels = []
    ann_text = list(nx.get_edge_attributes(G, "weight").values())
    #lbl_names = {}

    for i in G:
        labels.append(G._node[i]['id'])
        #lbl_names[i] = GraphModel._node[i]["name"]
        node_color = colormap_dict[G._node[i]['type']]
        colormap.append(node_color)

    return iG, colormap, labels, ann_text 
    