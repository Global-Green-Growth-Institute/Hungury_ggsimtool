#from msilib.schema import Directory
import numpy as np
import pandas as pd
import networkx as nx
from sklearn.preprocessing import minmax_scale
import igraph as ig
import os
os.environ["PATH"] += os.pathsep + './graphviz'


node_color_labels = ["GGI", "Edge Community"] # "Louvain Community", 
edge_color_labels = ["Edge Betweenness"]  #, "Infomap", "Walktrap"
n_measures = ["Degree", "Betweenness", "Closeness"] #, "Clustering"


def Network_Analysis_Tool(GraphModel, data, network_mode = "Direct", edge_mode = "Edge Betweenness"):
    """
        def Network_Analysis_Tool(GraphModel, data pic_name) converts the GraphModel to networkx and igraph networks, calculates the centrality measures of the direct graph(degree, closeness, betweenness) and the indirect graph (closeness, betweenness). It also clusters the graphs, and calculates the correlation matrix of the given and calculated data.
        Args:
            GraphModel (GraphModel.py): Created graphmodel
            data (pd.DataFrame): (optional) time series of input data. Set it to [] if quantitative analysis is not required.
            pic_name (str): names of the generated pictures 
        Returns:
            igraph.Graph: Converted Graphmodel (igraph)
            igraph.Graph: Graph of the indirect connections (igraph)
            igraph.clustering.VertexClustering: clustered iGraph 
            pd.DataFrame: Centrality Measures of both direct and indirect networks
            pd.DataFrame: Correlation matrix
    """
    
    # Define the colormap for the networkx presentation    
    colormap_dict = {'input' : '#00b4d9', 'output' : '#c70039', 'parameter' : '#ffc300', 'variable' : '#09ad03', 'computationnal' : '#BFBFBF' }
    colormap = []
    labels = []

    lbl_names = {}

    for i in GraphModel:
        labels.append(i)
        lbl_names[i] = GraphModel._node[i]["name"]
        node_color = colormap_dict[GraphModel._node[i]['type']]
        colormap.append(node_color)
        

    
    #lovain = nx.algorithms.community.louvain_communities(GraphModel)

    #to igraph
    g = ig.Graph.from_networkx(GraphModel)

    #iEigen = g.eigenvector_centrality() # cant calculated as it's directed and acyclic

    #igraph - indirect
    sh_path = np.array(g.shortest_paths()) #get the paths for eahc node
    c_adj = ~np.logical_or(sh_path == np.inf, sh_path== 0)*1 #convert to adjacency matrix - columns wil tell which nodes are connected to the selected output.



    #print(c_adj)
    dg = ig.Graph.Adjacency(c_adj) #Create a network from the adjacency

    G = []
    nG = []
    

    ##Adding k-cores, transitive closure, transitive reduction

    if network_mode == "Direct":
        G = g
        nG = GraphModel
    elif network_mode == "Indirect":
        G = dg
        nG = dg.to_networkx()
    elif network_mode == "k-core":
        G = g.k_core(4)
        nG = dg.to_networkx(G)
    #elif network_mode == "Transitive Reduction":
     #   nG = nx.transitive_reduction(GraphModel)
     #   G = ig.Graph.from_networkx(nG)       
    elif network_mode == "Summarization":
        nG = nx.dedensify(GraphModel)
        G = ig.Graph.from_networkx(nG)

    iBetweeness = G.betweenness() #betweenness
    iCloseness = G.closeness(mode='all') #closeness
    degree_cent = nx.degree_centrality(nG)
    net_clustering = nx.clustering(nG)

    #tr_cl= nx.transitive_closure(nG, reflexive=None)

    #print(tr_cl)

    #anc = nx.ancestors(nG)
    #desc = nx.descendants(nG)
    ### Community
    coms = []
    if edge_mode == "Edge Betweenness":
        coms = G.community_edge_betweenness(directed=True) 
        coms = coms.as_clustering()
    elif edge_mode == "Infomap":
        coms = G.community_infomap()
    elif edge_mode == "Walktrap":
        coms = G.community_walktrap()
        coms = coms.as_clustering()

    num_communities = len(coms)

    E=[e.tuple for e in G.es]# list of edges

    palette = ig.RainbowPalette(n=num_communities)
    edge_colormap = [None]*(len(E)+1) ### I d not know why but it needs a +1 to work...

    for i, community in enumerate(coms):
        G.vs[community]["color"] = i
        community_edges = G.es.select(_within=community)
        community_edges["color"] = i 
        for j in community:

            edge_colormap[j] = palette.get(i)     

    #create the centrality measure pd.DataFrame
    cent_measures = pd.DataFrame([list(degree_cent.values()), iBetweeness, iCloseness], index = ["Degree", "Betweenness", "Closeness"], columns =labels)
    cent_measures = pd.concat([cent_measures, pd.DataFrame(list(net_clustering.values()), columns = ["Clustering"], index = labels).transpose()])
    #cent_measures = pd.concat([cent_measures, pd.DataFrame(list(lovain.values()), columns = ["Louvain Communities"], index = labels).transpose()])

    ##Calculating the results of the graphs...
    if len(data) > 0:
        input_params = {}
        for i in GraphModel._node:
            if GraphModel._node[i]['type'] == 'input' :
                input_params[i] = np.delete(data.loc[i, :].to_numpy(), 0, 0)

        #get the results from the node computation
        results = GraphModel.run(input_params)
    else:
        results = pd.DataFrame([])

    return G, coms, cent_measures, colormap, edge_colormap, labels, results, lbl_names


def GetLouvainCommunity(igraph):
    N=len(igraph.layout(layout='auto'))
    G = igraph.to_networkx()

    coms = nx.algorithms.community.louvain.louvain_communities(G) # weight based on correlation
    num_communities = len(coms)

    palette = ig.RainbowPalette(n=num_communities)

    node_colormap = [None]*N
    for i, community in enumerate(coms):
        for j in community:
            node_colormap[j] = palette.get(i)
   
    return node_colormap

def GetEdgeCommunity(igraph_obj):
    """
    
    Note: colors nodes
    
    """
    layt = igraph_obj.layout(layout='auto')
    N=len(layt)
    
    coms = igraph_obj.community_edge_betweenness(directed=igraph_obj.is_directed()) 
    coms = coms.as_clustering()
    num_communities = len(coms)
    
    E=[e.tuple for e in igraph_obj.es]# list of edges
    palette = ig.RainbowPalette(n=num_communities)
      
    node_colormap = [None]*N
    for i, community in enumerate(coms):
        for j in community:
            node_colormap[j] = palette.get(i)
            
    return node_colormap


def GetCorrNetwork(corr_matrix, acceptance = 0.6, method = "pearson"):

    adj_mat = (np.abs(corr_matrix) > acceptance)*1
    np.fill_diagonal(adj_mat.values, 0)
    corr_g = nx.from_numpy_matrix(adj_mat.values, create_using=nx.Graph)

    corr_ig = ig.Graph.from_networkx(corr_g)
    layout = corr_ig.layout(layout='auto')

    E=[e.tuple for e in corr_ig.es]# list of edges
    corr_edge_colormap = []
    edge_weights = []
    for i in E:
        col = []
        if(corr_matrix.iloc[i] < 0):
            col = "rgb(255, 0, 0)"
        else:
            col = "rgb(0, 0, 255)"
        corr_edge_colormap.append(col)
        edge_weights.append((abs(corr_matrix.iloc[i])))
    

    ew = np.array(edge_weights)
    edge_weights = minmax_scale(ew).tolist() 
    return corr_ig, corr_edge_colormap, edge_weights
