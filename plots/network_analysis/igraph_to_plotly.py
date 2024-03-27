import igraph
import numpy as np
import pandas as pd
import networkx as nx
import igraph as ig
import warnings
import plotly.graph_objects as go
import os
import math
import random
#%% Converting the nodes from iGraph to plotly
def Vizualize_iGraph_Plotly(G,
                            labels,
                            node_colors,
                            weights = [],
                            edge_colors = None,
                            marker_scaler = [],
                            annotation_text = [],
                            marker_annonation = True,
                            names = [],
                            x_scale = 4,
                            y_scale = 2):
    random.seed(1234)

    #layt = nx.nx_pydot.pydot_layout(G, prog='dot')
    # g = ig.Graph.from_networkx(G)
    layt =G.layout_reingold_tilford(mode = "OUT") #G.layout(layout='')
    N=len(layt)
    
    if len(marker_scaler) == 0:
        marker_scaler = np.zeros(N).tolist()
    elif len(marker_scaler) != N:
        warnings.warn("The marker_scaler requires a %d length list of floats"% N)
      
    E=[e.tuple for e in G.es]# list of edges
    if len(annotation_text) == 0:
        annotation_text = ["" for i in range(len(E))]
    elif len(annotation_text) < len(E): 
            dummy = ["" for i in range(len(annotation_text), len(E))]
            annotation_text.append(dummy)
    

    Xn=[layt[k][0] for k in range(N)]
    Yn=[layt[k][1] *3 for k in range(N)]
    Xe=[]
    Ye=[]
    for e in E:
        Xe+=[layt[e[0]][0],layt[e[1]][0]]
        Ye+=[layt[e[0]][1]*3,layt[e[1]][1]*3]
    
    if edge_colors is None:
        edge_colors = ["rgb(0, 0, 0)" for i in range(math.ceil(len(Xe)/2))]
        
    if len(weights) == 0:
        weights = [0 for i in range(math.ceil(len(Xe)/2))]
    
    
    fig = go.Figure()
    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )
    fig.update_xaxes(axis)
    fig.update_yaxes(axis)
    
    for i in range(N):

        lbl = labels[i]
        if len(names) != 0:
            lbl_name = names[labels[i]]

        fig.add_trace(go.Scatter(
            mode='markers', x=[Xn[i]], y=[Yn[i]],
            marker=dict(color=node_colors[i], size=25 + marker_scaler[i]*30 ,
                line=dict(
                    color='black',
                    width=1)
            ),
            text=lbl,
            hoverinfo='text',
            showlegend=False)
            )
        if marker_annonation:
            fig.add_annotation(x=Xn[i],  # arrows' head
                               y=Yn[i] + 1,  # arrows' head
                               ax=Xn[i],  # arrows' tail
                               ay=Yn[i],  # arrows' tail
                               xref='x',
                               yref='y',
                               axref='x',
                               ayref='y',
                               showarrow=False,
                               text=str(np.round( marker_scaler[i], decimals=4)),)

        if node_colors[i] !='#BFBFBF':
             fig.add_annotation(x=Xn[i],  # arrows' head
             y=Yn[i],  # arrows' head
             ax=Xn[i],  # arrows' tail
             ay=Yn[i],  # arrows' tail
             xref='x',
             yref='y',
             axref='x',
             ayref='y',
             showarrow=False,
             text= lbl,)
        fig.update_traces(textfont_size=18)
    j=0   
    ar = 5
    if G.is_directed() == False:
        ar = 0
    for i in range(0, len(Xe), 2):
        color = []
        if type(edge_colors[j]) == tuple:
            col = np.floor(np.array(edge_colors[j])*255).astype(int).tolist()
            color = "rgb(" + str(col[0]) + ", " + str(col[1]) + ", "+ str(col[2]) + ")" #+ ", "+str(col[3])
        else:
            color = edge_colors[j]
        fig.add_annotation(
          x=Xe[i+1],  # arrows' head
          y=Ye[i+1],  # arrows' head
          ax=Xe[i],  # arrows' tail
          ay=Ye[i],  # arrows' tail
          xref='x',
          yref='y',
          axref='x',
          ayref='y',
          #text= annotation_text[j],
          showarrow=True,
          arrowhead=ar,
          arrowsize=1,
          arrowwidth=1 + weights[j]*6,
          arrowcolor=color
        )

        if annotation_text[j] != "":
            fig.add_annotation(
            x=Xe[i],  # arrows' head
            y=Ye[i],  # arrows' head
            ax=Xe[i] +0.5,  # arrows' tail
            ay=Ye[i] +0.5,  # arrows' tail
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            text= annotation_text[j],
            arrowwidth=0.1,
            arrowcolor=color
            )
        j = j+1
    fig.update_layout(paper_bgcolor="rgba(1,1,1,0)", plot_bgcolor="rgba(1,1,1,0)")
    fig.update_layout(width=x_scale*1000, height=y_scale*500,)
    #fig.show()
    return fig

#%% Plotly heatmap
def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()}
