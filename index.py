# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings('ignore')

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

from pages import (
    country_overview,
    data_viz,
    model_overview,
    #country_comparator,
    system_dynamic_models,
    Experts,
    #spatial,
    open_code,
    downloads,
    Network_Analysis,
    shap,
    CorrelationalAnalysis
)


app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

server = app.server

# Update page

@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def display_page(pathname):
    #if pathname == "/SimulationDashBoard/regional-outlouk":
       # return regional_outlook.layout
    #elif pathname == "/SimulationDashBoard/country-comparator":
        #return country_comparator.layout
    if pathname == "/SimulationDashBoard/models":
        return model_overview.layout
    elif pathname == "/SimulationDashBoard/downloads":
        return downloads.layout
    #-----------------------------------------
    #elif pathname =="/projects":
       # return projects.layout
    elif pathname == "/SimulationDashBoard/data":
        return data_viz.layout
    elif pathname == "/SimulationDashBoard/codes":
        return open_code.layout
    elif pathname == "/SimulationDashBoard/system-dynamic-models":
        return system_dynamic_models.layout
    elif pathname == "/SimulationDashBoard/Network-Analysis":
        return Network_Analysis.layout
    elif pathname == "/SimulationDashBoard/ShapNet":
        return shap.layout
    elif pathname == "/SimulationDashBoard/CorrelationalAnalysis":
        return CorrelationalAnalysis.layout    
    elif pathname == "/SimulationDashBoard/Experts":
        return Experts.layout
    else:
        return country_overview.layout
    pass


if __name__ == "__main__":
        app.run_server(debug=True,
        
                   host='localhost',
                   port=8080,
                   # dev_tools_ui=False,
                   # dev_tools_props_check=False,
                   )
