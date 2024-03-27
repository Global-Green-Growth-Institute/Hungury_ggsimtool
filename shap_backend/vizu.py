
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import warnings
import math

import networkx as nx
import igraph as ig

def GetEWNodeColor(change_expl, node_names):
    """This function returns the node colors for the graph. It is based on the change_expl dictionary. HARDCODED FOR EW MODEL!
    ## Args:
    - change_expl (dict[var_name:str, pd.DataFrame]): dictionary of the explainability values -> dependency injection, it IS a global variable required for the analysis.
    - node_names (list[str]): list of node names
    ## Returns:
    - color_dict (list[tuple]): list of nodes with their colors, labels and shapes
    """

    color_dict = []
    for i in node_names:
        col = "orange"
        sh = "triangle-up"
        lbl = i
        if i == "MWU" or  i == "Cr":
            sh = "hexagon2"
        
        if i == "WP" or i == "IRRTECHi_Drip" or i == "IRWR" or i == "ERWR" or i == "AIR":
            col = "green"
        elif i == "EW1":
            col = "yellow"
            lbl = "SDG 6.4.1"
            
        elif i == "EW2":
            col = "yellow"
            lbl = "SDG 6.4.2"
        elif i in list(change_expl.keys()):
            col = "blue"
            
        color_dict.append( (i, {"color": col, "shape": sh, "label" : lbl}))
    
    return color_dict


def GetShapWeight(change_expl):
    """This function returns the edge weights for the graph. It is based on the change_expl dictionary.
    ## Args:
    - change_expl (dict[var_name:str, pd.DataFrame]): dictionary of the explainability values -> dependency injection, it IS a global variable required for the analysis.
    ## Returns:
    - scaled_change_expl (dict[var_name:str, pd.DataFrame]): dictionary of normalized explainability values"""
    scaled_change_expl = change_expl.copy()
    for k,v in change_expl.items():
        if np.sum(v) != 0:
            change_expl[k] =  v/np.sum(np.abs(v))
    return scaled_change_expl 



def GetShapEdges(input_vars, shapley, change_expl, row_ind = None):
    """This function returns the edges for the graph.
    ## Args:
    - input_vars (dict[str, list[str]]): dictionary of which output variable requires which input variable
    - shapley (dict[var_name:str, np.ndarray]): dictionary of the shapley values
    - change_expl (dict[var_name:str, np.ndarray]): dictionary of the explainability values
    - row_ind (int): row index for the shapley values -> will define which row to use for the edge weights. If None, then the mean of values wioll be used.
    ## Returns:
    - edge_color (list[tuple]): list of edges with their weights, widths and colors
    """
    edge_color = []
    for k,v in input_vars.items():
                    if not isinstance(shapley[k], dict):
                        #shapl =shapley[k].values[19, :]  # np.mean(np.abs(shapley[k].values), axis = 0)
                        for idx, j in enumerate(v):
                            # if shapl[idx] is np.nan:
                            #     print(k + "_" +j)
                            if len(j) != 0:
                                    #e.edge(j, k)
                                    col = "grey"
                                    weight = 0
                            
                                    if row_ind == None:
                                        
                                        weight = pd.Series(change_expl[k]).iloc[idx]
                                        if weight != 0:
                                            col= "black"
                                            edge_color.append((j,k, {"weight": [weight/np.sum(np.abs(pd.Series(change_expl[k])))], "edge_color" : col, "edge_width" : [weight*5/np.sum(np.abs(pd.Series(change_expl[k])))]}))
                                        else:
                                            edge_color.append((j,k, {"weight": [weight], "edge_color" : col, "edge_width" : [0]}))
                                        
                                    else:
                                        if type(shapley[k]) != np.ndarray:
                                                #col = "black"
                                                weight = pd.DataFrame(shapley[k].values).iloc[row_ind, idx]#/np.abs(pd.DataFrame(shapley[k].values).iloc[row_ind, :].sum())
                                                sign = 1
                                                if pd.DataFrame(shapley[k].values).iloc[row_ind, idx] < 0:
                                                    col = "#0080FF"
                                                    sign = -1
                                                elif pd.DataFrame(shapley[k].values).iloc[row_ind, idx] > 0:
                                                    col = "#FF0070"
                                                #print("____")
                                                #print(pd.DataFrame(shapley[k].values).iloc[row_ind, idx])
                                                #print(np.sum(np.abs(pd.DataFrame(shapley[k].values).iloc[row_ind, :])))
                                                edge_color.append((j,k, {"weight": [sign*np.abs(weight)/np.sum(np.abs(pd.DataFrame(shapley[k].values).iloc[row_ind, :]))], "edge_color" : col, "edge_width" :  [np.abs(weight)*5/np.sum(np.abs(pd.DataFrame(shapley[k].values).iloc[row_ind, :]))]}))
                                        else:
                                            edge_color.append((j,k, {"weight": [0], "edge_color" : "grey", "edge_width" :  [0]}))
                                        
    return edge_color
#%%
def BuildGraph(change_expl, node_names, input_vars, shapley, row_ind = 17):
    """This function builds the networkx graph based on the inputs.
    ## Args:
    - change_expl (dict[var_name:str, np.ndarray]): dictionary of the explainability values -> dependency injection, it IS a global variable required for the analysis.
    - node_names (list[str]): list of node names
    - input_vars (dict[str, list[str]]): dictionary of which output variable requires which input variable
    - shapley (dict[var_name:str, np.ndarray]): dictionary of the shapley values
    - row_ind (int): row index for the shapley values -> will define which row to use for the edge weights. If None, then the mean of values wioll be used.
    ## Returns:
    - G (networkx.DiGraph): networkx graph
    """
    G = nx.DiGraph()
    G.add_nodes_from(GetEWNodeColor(change_expl, node_names))
    G.add_edges_from(GetShapEdges(input_vars, shapley, change_expl, row_ind=row_ind))
    
    return G


def ToiGraph(G):
    """This function converts the networkx graph to igraph graph. It also used graphviz for hierarchical tree-like layout.
    ## Args:
    - G (networkx.DiGraph): networkx graph
    ## Returns:
    - g (igraph.Graph): igraph graph
    - ll (igraph.Layout): layout of the graph
    """
    layy = nx.nx_pydot.pydot_layout(G, prog='dot')
    ll = ig.Layout(list(layy.values()))
    g = ig.Graph.from_networkx(G)
    
    return g, ll
    
                                    
#%%

def Vizualize_iGraph_Plotly(G, layt,  marker_scaler = [], show_weight = True, show_node_size = False, scale_node_size = True, x_scale =1.3, y_scale = 1.6):
    """This function vizualizes the igraph graph using plotly.
    ## Args:
    - G (igraph.Graph): igraph graph
    - layt (igraph.Layout): layout of the graph
    - marker_scaler (list[float]): list of marker size for the nodes
    - show_weight (bool): show the edge weights
    - show_node_size (bool): show the node size (float value, can clutter with weight numbers)
    - scale_node_size (bool): scale the node size
    - x_scale (float): x scale of the graph
    - y_scale (float): y scale of the graph
    ## Returns:
    - fig (plotly.graph_objects.Figure): plotly figure
    """
    ## Get node data from igraph
    N=len(layt)
    node_colors = G.vs["color"]
    marker_shape = G.vs['shape']
    labels = G.vs["label"]
    names = []
     
    ## Get edge data from igraph
    edge_colors = G.es["edge_color"]
    weights = G.es["weight"]
    widths =  G.es["edge_width"]
    
    # If there is no marker_scaler, then set it to 0
    if len(marker_scaler) == 0:
        marker_scaler = np.zeros(N).tolist()
    elif len(marker_scaler) != N:
        warnings.warn("The marker_scaler requires a %d length list of floats"% N)
    else:
        # If scaling nodes is allowed, then scale the node size
        if scale_node_size:
            marker_scaler =  np.array(marker_scaler) / max(marker_scaler)
    ## If there is a nan value, then set it to 0
    if np.sum(np.isnan(np.array(marker_scaler))*1) > 0:
          asd = np.array(marker_scaler)
          asd[np.isnan(np.array(marker_scaler))] = 0
          marker_scaler = asd.tolist()
          
    ## Get edge data from igraph
    E=[e.tuple for e in G.es]# list of edges

    ## Get node positions from igraph based on the layout provided by graphviz
    Xn=[layt[k][0] for k in range(N)]
    Yn=[layt[k][1] for k in range(N)]
    Xe=[]
    Ye=[]
    ## Get edge positions from igraph based on the layout provided by graphviz
    for e in E:
        Xe+=[layt[e[0]][0],layt[e[1]][0]]
        Ye+=[layt[e[0]][1],layt[e[1]][1]]
    
    
    ## If there is no edge weight, then set it to 0
    if len(weights) == 0:
        weights = [0 for i in range(math.ceil(len(Xe)/2))]
    
    #Make an empty figure and start filling it up with relevant information.
    fig = go.Figure()
    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )
    fig.update_xaxes(axis)
    fig.update_yaxes(axis)

    #For each Node:
    for i in range(N):
        lbl = labels[i]
        shape = marker_shape[i]
        if len(names) != 0:
            lbl = names[labels[i]]
        ## Add a scatter point with the specified size, shape, label and color
        fig.add_trace(go.Scatter(
            mode='markers', x=[Xn[i]], y=[Yn[i]],
            marker=dict(color=node_colors[i], size=25 +  np.clip( marker_scaler[i]*50, 0, 80),
                line=dict(
                    color='black',
                    width=2)
            ),
            marker_symbol=shape,
            text=lbl,
            hoverinfo='text',
            showlegend=False)
            )

    # Set arrow head to 5 if the graph is directed
    ar = 5
    # If the graph is undirected, then set the arrow head to 0 (so that there is no direction)
    if G.is_directed() == False:
        ar = 0

    # For each edge:
    for j, i in enumerate(range(0, len(Xe), 2)):
        color = []
        if type(edge_colors[j]) == tuple:
            col = np.floor(np.array(edge_colors[j])*255).astype(int).tolist()
            color = "rgb(" + str(col[0]) + ", " + str(col[1]) + ", "+ str(col[2]) + ")" #+ ", "+str(col[3])
        else:
            color = edge_colors[j]
        ## Add an edge with the specified width, color and weight
        fig.add_annotation(
          x=Xe[i+1],  # arrows' head
          y=Ye[i+1],  # arrows' head
          ax=Xe[i],  # arrows' tail
          ay=Ye[i],  # arrows' tail
          xref='x',
          yref='y',
          axref='x',
          ayref='y',
          #text=str(np.round(weights[j][0], decimals = 4)),
          showarrow=True,
          arrowhead=ar,
          arrowsize= 0.5,
          arrowwidth=1 + widths[j][0],
          arrowcolor=color
        )
        ## create weight label in the middle of the edge
        if show_weight:
            fig.add_annotation(
              x=Xe[i+1] -(Xe[i+1]- Xe[i]) /2,  # arrows' head
              y=Ye[i+1]-(Ye[i+1]- Ye[i]) /2,  # arrows' head
              ax=Xe[i+1] -(Xe[i+1]- Xe[i]) /2,  # arrows' tail
              ay=Ye[i+1] -(Ye[i+1]- Ye[i]) /2,  # arrows' tail
              xref='x',
              yref='y',
              axref='x',
              ayref='y',
              font=dict(
                  family="Arial, monospace",
                  color = color,
                  size=16
                  ),
              text= str(np.round(weights[j][0], decimals = 4)),
              showarrow=False,
              bgcolor="#FFFFFF",
              #arrowhead=ar,
              #arrowsize=0.5,
              #arrowwidth=1 + float(widths[j][0]),
              #arrowcolor=color
            )
    ## Add node labels
    # The reason this is done separately is because the node labels are not part of the scatter plot, but rather a separate annotation, and so glithces can occur
    # e.g. edges over the label make it unreadable
    for i in range(N):
            lbl = labels[i]
            ss = 16
            # if the variable name is too long, then reduce the font size
            if len(lbl) > 5 and len(lbl) <= 10:
                ss = 12
            elif len(lbl) > 10:
                ss = 8
            
            fig.add_annotation(x=Xn[i],  # arrows' head
            y=Yn[i] - 15,  # arrows' head
            ax=Xn[i],  # arrows' tail
            ay=Yn[i],  # arrows' tail
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            showarrow=False,
            font=dict(
                size=ss,
                color=color
                ),
            text= "<b>" + lbl + "<b>",)
            ## Add node size label that represents weight of a node
            if show_node_size:
                fig.add_annotation(
                    x=Xn[i],  # arrows' head
                    y=Yn[i]+30,  # arrows' head
                    ax=Xn[i],  # arrows' tail
                    ay=Yn[i],  # arrows' tail
                    xref='x',
                    yref='y',
                    axref='x',
                    ayref='y',
                    font=dict(
                          family="Arial, monospace",
                          color = "black",
                          size=16
                          ),
                    text=str(np.round(marker_scaler[i], decimals = 4)),
                    showarrow=False
                )
    ## update the figure.
    fig.update_traces(textposition='middle center')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(paper_bgcolor="rgba(1,1,1,0)", plot_bgcolor="rgba(1,1,1,0)")
    fig.update_layout(width=x_scale*1000, height=y_scale*500,)

    return fig