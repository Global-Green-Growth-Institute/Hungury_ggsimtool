import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table


import dash
from dash.dependencies import Input, Output
from app import app, data, INDEX_YEAR, MIN_YEAR
from pages import model_overview

#from utils import Header
from utils import Header, Footer

import numpy as np
import pandas as pd
# new imports
import pages.network_analysis_tool as nat
import plots.network_analysis.igraph_to_plotly as itop
import data_utils as du
from utils import is_btn_clicked

from ggmodel_dev.models.greengrowth import GGGM
import plotly.graph_objects as go
import json

# set the figure size 
fig_network1=go.Figure()
fig_network1.update_layout(width=700,height=700)

#%% Import the models, and their properties.
prop_files = ["Energy/Energy_properties.json", "Energy/Installed_properties.json", "Energy/Intensity_properties.json", "landuse/BE2_properties.json", "landuse/BIOGAS_properties.json", "landuse/BIOMASS_properties.json", "landuse/NUTRIENT_properties.json", "water_model/EW_hungary_properties.json"]
all_props = {}
for i in prop_files:
    f = open('ggmodel_dev/models/' + i,encoding="utf8")
    props_dummy = json.load(f)
    f.close()
    #all_props = {key: value for (key, value) in (all_props.items() + props_dummy.items())}
    for key, vals in props_dummy.items():
        all_props[key] = vals


networks = GGGM.all_model_dictionary

#print(data)



network_names = {}
#req_data = []
# We will use this to generate the options for the networks...
model_list = all_props.keys()
for model_name, model in networks.items():
    mds = [model_name == i for i in model_list]
    if any(mds):
        network_names[model_name] = model 
    #for i in model._node:
        #if model._node[i]['type'] == 'parameter':
            #req_data.append(model_name + ": " +  str(model._node[i]['name']))

#pd.DataFrame(req_data).to_excel("param_req_data.xlsx")   

network_names_dropdown = []
for y in network_names.keys():
    try:
        network_names_dropdown.append({'label': all_props[y]["display_name"], 'value': y})

    except:
        network_names_dropdown.append({'label': y, 'value': y})
    #network_names_dropdown.append({'label': GGGM.all_model_properties[y]['display_name'], 'value': y})

 #%% Data -temporary solution...

network_mode = [{'label':"Direct", 'value': "Direct"}] #, {'label':"Indirect", 'value': "Indirect"}


size_labels = []
for i in nat.n_measures:
    size_labels.append({'label':i, 'value': i})


node_color_labels = []
for i in nat.node_color_labels:
    node_color_labels.append({'label':i, 'value': i})


edge_color_labels = []
for i in nat.edge_color_labels:
    edge_color_labels.append({'label':i, 'value': i})


na_settings = { 'network' : [],
                'network_mode' : [],
                'node_size' :  [],
                'node_size_slider' : INDEX_YEAR,                
                'node_color' : [],
                'edge_color' : []
}

na_set_desc = {"Direct" : "Direct mode: Only the predefined connections are seen between nodes.", 
            "Indirect" : "Indirect mode: A node is connected to the variables it has an impact on.", 
            "Degree" : "A centrality measure that calculates how many neighbors a node has, which may show how important the node is. Relevancy: One can find the major variables that play an important role in the ecosystem. (e.g. renewable, non-renewable energies)", 
            "Betweenness" : "A centrality measure that calculates the shortest paths between the nodes. The more of the shortest paths go through the node, the higher the centrality is. Relevancy: How important",
            "Closeness" : "Measures how close can one node be found to the other nodes. Reveals the nodes with the most (indirect) connections.",
            "Clustering": "Under development. Most probably I'll take this out.",
            "GGI" : html.Div([
                html.Div    ([ "The standard color scheme of GGGI's graphs."]),
                html.Div    ([ "Green: Simulated variables"], style={"color": '#09ad03'}),
                html.Div    ([ "Yellow: Parameters"], style={"color": "#ffc300"}),
                html.Div    ([ "Red: Outputs"], style={"color": '#c70039'}),
                html.Div    ([ "Grey: Computational nodes"], style={"color": "#BFBFBF"}),
                html.Div    ([ "Blue: Input variables"], style={"color": '#00b4d9'}),
            ]) ,
            "Louvain Community" : "Detects communities in the networks through the Louvain greedy optimization method.",
            "Edge Community": "Detects communities in the networks based on the connections between the nodes. The same color shows which nodes are in the same group. ",
            "Edge Betweenness" : "Calculates the shortest paths between edges. Groups similar edges.",
            "Infomap": "Partitions the edges into different groups. Groups similar edges.",
            "Walktrap": "Finds densely populated subnetworks through random walks."
             }
            
#%% Layouts

layout = html.Div(
    [
        html.Div([
            Header(app, 'Network Analysis')
        ]),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Highlights"),
                                html.Br([]),
                                html.P("Network analysis is a set of integrated techniques to depict relations among actors and to analyze the social structures that emerge from the recurrence of these relations.",
                                       style={"color": "#ffffff", 'font-size': '15px'},),
                                html.Br([]),
                                html.P("Network Analysis converts the GraphModel to Networkx and igraph networks, and calculates the centality measures of the direct graph (degree,closeness,betweenness). It also clusters the graphs,and calculates the correlation matrix of the given and calculated data. In the figures, the number over the nodes denote centrality value.",
                                       style={"color": "#ffffff", 'font-size': '15px'})
                                       
                            ],
                            className="product"
                        ),


                        html.Div(
                            [
                                html.Br([]),
                                html.Div(children='Select Network'),
                                dcc.Dropdown(id='network_sel_dropdown',options=network_names_dropdown, value = list(GGGM.all_model_dictionary.keys())[0], placeholder=list(GGGM.all_model_dictionary.keys())[0]),
                                html.Div(id='network_desc', children=["Network Description"]),
                                html.Br([]),
                                html.Div(children='Network Mode'),
                                dcc.Dropdown(id='network_mode_dropdown', options = network_mode, value = network_mode[0]['value'], placeholder=network_mode[0]['value']),
                                html.Div(id='network_mode_desc', children=["Network Mode Description"]),  
                                html.Br([]),
                                html.Div(children='Node Size'),
                                dcc.Dropdown('variable_size_dropdown', options = size_labels, value =size_labels[0]['value'],  placeholder=size_labels[0]['value']),
                                #dcc.Slider(min=int(years_labels[0]), max=int(years_labels[-2]), step=1, value=int(years_labels[0]), id='variable_size_slider', marks =years_markdown, updatemode='mouseup'),
                                
                                html.Div(id='node_size_desc', children=["Node Size Description"]),      
                                html.Div(children='The annotations above nodes denote the corresponding centrality values.'),
                                html.Br([]),
                                #dcc.Slider(min=MIN_YEAR, max=2050, step=10, value=INDEX_YEAR, id='variable_size_slider', marks = ["2000", "2010", "2020", "2030", "2040", "2050"] ,  updatemode='mouseup'),

                                html.Br([]),
                                html.Div(children='Node Color'),
                                dcc.Dropdown(id='node_color_dropdown', options = node_color_labels, value = node_color_labels[0]['value'], placeholder=node_color_labels[0]['value']),
                                html.Div(id='node_color_desc', children=["Node Color Description"]),
                                html.Br([]),
                                # html.Div(children='Edge Color'),
                                # dcc.Dropdown(id='edge_color_dropdown', options = edge_color_labels, value = edge_color_labels[0]['value'], placeholder= edge_color_labels[0]['value']),
                                # html.Div(id='edge_color_desc', children=["Edge Color Description"]),
                                # html.Br([]),
                                html.Button('Run', id='btn-run', n_clicks=0,
                                style={'font-size': 20,
                                       'font-weight': 'normal',
                                       'color': '#ffffff',
                                       'background': '#14ac9c',
                                       'border': '#14ac9c',
                                       }) #,
                                #html.Br([]),
                                #html.Button('Download', id='btn-dwn', n_clicks=0,
                                #style={'font-size': 20,
                                #       'font-weight': 'normal',
                                #       'color': '#ffffff',
                                #       'background': '#14ac9c',
                                #       'border': '#14ac9c',
                                #       }),
                                #dcc.Download(id="download-netw")

                            ], className="na_ui"

                        )
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.H5("Network Analysis results:"),
                        html.Br([]),
                        dcc.Graph(id='network',figure=fig_network1, responsive=True),

                    ],
                    className="pretty_container eight columns"
                ),

            ],
            className="row",
        ),
        Footer(),
    ],
    className="page",
)
@app.callback(
    Output("download-netw", "data"),
    Input("btn-run", "n_clicks"),
    Input('network', 'figure'),
    prevent_initial_call=True
)
def down_network(n_clicks, fig):
    if(is_btn_clicked('btn-dwn')):
        fig.write_html("./images/export.html")
        return dcc.send_file("./images/export.html")

###
@app.callback(
    #Output('network_desc', 'children'),
    Output('network_mode_desc', 'children'),
    Output('node_size_desc', 'children'),
    Output('node_color_desc', 'children'),
    #Output('edge_color_desc', 'children'),
    Input('network_sel_dropdown', 'value'),
    Input('network_mode_dropdown', 'value'),
    Input('variable_size_dropdown', 'value'),
    Input('node_color_dropdown', 'value'),
    #Input('edge_color_dropdown', 'value')
)
def change_network_setting(net, net_mode, node_size, node_col): #, edge_col
    
    # print("------------")
    
    # print("Selected network:")
    # print(net)
    # print(networks[net])
    na_settings['network'] = networks[net]

    # for i in networks[net]._node:
    #     #print(i)
    na_settings['network_mode'] = net_mode
    #na_settings['edge_color'] = edge_col
    na_settings['node_size'] = node_size
    na_settings['node_color'] = node_col
    return na_set_desc[net_mode], na_set_desc[node_size], na_set_desc[node_col]#, na_set_desc[edge_col] # GGGM.all_model_properties[net]['description'],
###


@app.callback(
    Output("index-table", "style_data_conditional"),
    Input("index-table", "active_cell"),
)
def style_selected_rows(active_cell):
    if active_cell is None:
        return dash.no_update

    css = [
        {'if': {'row_index': 'odd'},
    'backgroundColor': 'rgb(0, 0, 0, 0.1)',
        },
        {"if": {'row_index': active_cell['row']},
            "backgroundColor": "rgba(45, 178, 155, 0.3)",
            "border": "1px solid green",
            },
           {
        # 'active' | 'selected'
        "if": {"state": "selected"},
        "backgroundColor": "rgba(45, 178, 155, 0.3)",
        "border": "1px solid green",
    }, 
    
    ]
    return css


@app.callback(
    Output('network', 'figure'),
   #Output('variable_size_slider', 'disabled'),
    Input("btn-run", "n_clicks")
)
def update_variable_network(n_clicks):
    if(is_btn_clicked('btn-run')):

            #print("Button Pressed")

            variable_size_dropdown = na_settings['node_size']
            #variable_size_slider =[2000, 2005, 2010, 2015, 2020]
            network_mode_dropdown = na_settings['network_mode']
            sel_model = na_settings['network']
            node_col = na_settings['node_color']
            #edge_col = na_settings['edge_color']


            dat = []

            G, _, cm, cl, e_cl, labels, results, lbl = nat.Network_Analysis_Tool(sel_model, dat, network_mode = network_mode_dropdown)
            mark_sc ={}
            #dis_slider = True
            
            #print("Setting Node color")
            if node_col == "Louvain Community":
                cl = nat.GetLouvainCommunity(G)
            elif node_col == "Edge Community":
                cl = nat.GetEdgeCommunity(G)        

            #print("Get node size vars")
            #if variable_size_dropdown == 'Year':
             #   dis_slider = False
             #   for i in labels:
             #       dummy = results.get(i)
             #       if dummy is None:
             #          mark_sc[i] = 0
             #       else:
             #           mark_sc[i] = float(dummy[int(variable_size_slider)-2000])
            #else:
            #    for i in labels:
            #        mark_sc[i] = cm.loc[variable_size_dropdown, i]
            
            for i in labels:
                    mark_sc[i] = cm.loc[variable_size_dropdown, i]
            dat = pd.DataFrame.from_dict(mark_sc, orient='index')
            pd_mark_sc = []
            if dat.sum().sum() != 0:
                pd_mark_sc = (dat/dat.max()).to_numpy().tolist()
            else:
                pd_mark_sc = np.zeros((len(labels), 1)).tolist()
            mark_sc = [float(x[0]) for x in pd_mark_sc]
            fig1 = itop.Vizualize_iGraph_Plotly(G, labels, cl,  marker_scaler = mark_sc, names = lbl) #edge_colors = e_cl,

    else: fig1 = go.Figure()
    return  fig1#, dis_slider