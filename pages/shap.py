import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table

import dash
from dash.dependencies import Input, Output
from app import app, data, INDEX_YEAR, MIN_YEAR
from pages import model_overview

# from utils import Header
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
import pickle
import os
# set the figure size


# %% Layouts

shap_fig_dir = os.path.join(os.getcwd(),"shap_backend", "figs")
models = ["EW"] ## Here comes the model name for which a SHAP analysis is implemented (also the name of the directory e.g. "EW")

### Load figs to memory:
shap_figs = {}
for model in models:
    shap_figs[model] = {}
    for file in os.listdir(os.path.join(shap_fig_dir, model)):
        if file.endswith(".pkl"):
            with open(os.path.join(shap_fig_dir, model, file), "rb") as f:
                shap_figs[model][file[:-4]] = go.Figure(pickle.load(f))

start_year = 2000
end_year = 2020


subtypes = [{"label": str(start_year + i), "value" : str(i)} for i in range(end_year - start_year)]
subtypes.append({"label" : "Mean", "value" : "mean"})
centrality_type = [ {"label": "None", "value": "None"},
                    {"label": "Degree Centrality", "value": "degree"},
                    {"label": "Closeness Centrality", "value": "closeness"},
                    {"label": "Betweenness Centrality", "value": "betweenness"}]

#
# subtypes = {"mean" : [],
#             "ind" : [{"label": str(start_year + i), "value" : str(i)} for i in range(end_year - start_year)],
#             "ct" : [{"label": "Degree Centrality", "value": "degree"},
#                     {"label": "Closeness Centrality", "value": "closeness"},
#                     {"label": "Betweenness Centrality", "value": "betweenness"}]}

layout = html.Div(
    [
        html.Div([
            Header(app, 'ShapNet')
        ]),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Highlights"),
                                html.Br([]),
                                html.P(
                                    """The SHAP-based network analysis is a method to identify key variables and validate expert-based models.
                         The Shapley value measures the contribution of each variable to the output/calculated variable of the hierarchical model.
                         Generally speaking, the Shapley value is a measure of the marginal contribution of a variable to the change in the output. If the expected value (e.g. average of a variable) and the value of the variable are the same, the Shapley value would be 0.
                         Therefore, the Shapley value can be used to define high-impact, relevant variables that can be used to identify optimal intervention points (policies) based on their systematic exploration and impact of the contribution on the SDG output.
                         This systematic exploration can also be used to check the effectiveness of existing policies, as the Shapley values first analyses data yearly. This way, year-specific evaluation may provide an insight to possible evolution of the model. 
                         It also provides means to evaluate trends by taking the average of the absolute Shapley values over the years, which may establish the general importance (trend) of a variable.""",
                                    style={"color": "#ffffff", 'font-size': '15px'}, ),

                            ],
                            className="product"
                        ),

                        html.Div(
                            [
                                html.Div(children="Select dynamical model:"),
                                dcc.Dropdown(id='shap_model_sel', options=[{"label": "EW", "value": "EW"}], value="EW",
                                             placeholder="EW"),
                                html.Div(children="Select the type of analysis:"),
                                dcc.Dropdown(id='shap_type_sel', options=subtypes,
                                             value="mean"),
                                html.Div(children="Select centrality measure type:"),
                                ## This tab will dinamically change with the specific type of analysis
                                dcc.Dropdown(id='shap_param_sel',
                                             options=centrality_type, value="None"),
                                html.Div(children="Color Scheme Legend:"),
                                html.Div("Red edge (->) : Positive SHAP value (weight of edge)", style={"color": "#FF0070"}),
                                html.Div("Blue edge (->) : Negative SHAP value (weight of edge)", style={"color": "#0080FF"}),
                                html.Div("black edge (->) : mean of absolute SHAP values (weight of edge)", style={"color": "#000000"}),
                                html.Div("grey edge (->) : SHAP value = 0 (weight of edge)", style={"color": "#808080"}),
                                html.Div("Blue node : Calculated variable", style={"color": "#0000ff"}),
                                html.Div("Green node : Input variable", style={"color": "#00ff00"}),
                                html.Div("Orange node : Input variable as possible intervention point", style={"color": "#ffa500"}),
                                html.Div("Yellow node : Output variable", style={"color": "#ffff00", "background-color" : "#808080"}),
                                html.Div("Triangle node : Unparameterized function", style={"color": "#000000"}),
                                html.Div("Hexagon node : Parameterized function (can be optimized)", style={"color": "#000000"}),

                                html.Br([]),
                                html.H5(
                                    "Description of SHAP-based network analysis for dynamical models:"),

                                html.Div("""The method contains network analysis-based approach as well. The nodes represent variables, and edge connection defines an input-output relationship. The edge weights are normalized with the total amount of contribution, in both individual and trend cases.
The size of the nodes may provide information about the importance of the variable depending on which centrality measure is used. 
Degree centrality defines the number of incoming and/or outgoing edges - how many elements are affected, how many elements are affected? 
Closeness defines distance from a node - How short are the closest paths in the other variables? 
Betweenness answers the questions of How many critical paths pass through a variable? How inevitable is the variable?These values depend on the weight, so we can determine the key variables."""),

                                html.Div("""Figures show that there are aggregated and raw data input sources
to describe the aggregated SDG indicators, which can be used to identify optimal
intervention points (policies) based on their systematic exploration and impact of the
contribution on the SDG output, and this systematic exploration can also be used to
check the effectiveness of existing policies."""),
                                html.Div("""The types of nodes are represented with different colors and
shapes (green triangle - policy intervention points; orange triangle - input variables; blue triangle - variables; blue hexagon - variables with parameters;
yellow triangle - output). The thickness of the arrows represents the strength of contribution.""")
                            ], style={"height": "100%", "width": "100%"}),

                            ], className="shap_ui"

                        )
                    ],
                    className="pretty_container three columns"
                ),
                html.Div(
                    [
                        html.H5("Shapley value based evaluation of networks:"),
                        html.Br([]),
                        html.Div([
                            dcc.Graph(id='shapnet_graph', figure=go.Figure(), responsive=True, style={"height": "100vw", "width": "70vw"}),
                            html.Br([]),
                    ],
                    className="pretty_container nine columns"
                ),


            ],
            className="row",
        ),
        Footer(),
    ],
    className="page",
)


@app.callback(
    Output('shapnet_graph', 'figure'),
    [Input('shap_model_sel', 'value'),
     Input('shap_type_sel', 'value'),
     Input('shap_param_sel', 'value')])
def update_shapnet_graph(model, type, centrality):
    fig = go.Figure()
    fig_name = "shap_net_" + type + "_" + centrality
    return shap_figs[model].get(fig_name, go.Figure())
