from os import link
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from utils import Header, Footer, MyHeader
from app import app

layout = html.Div([
    html.Div([MyHeader(app, 'Codes')]),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Global', value='tab-1-example-graph',style={"color":"black", 'font-weight': 'bold', 'font-size': '15px' } ),
        dcc.Tab(label='Regional', value='tab-2-example-graph',style={"color":"black", 'font-weight': 'bold', 'font-size': '15px' }),
        dcc.Tab(label='National', value='tab-3-example-graph',style={"color":"black", 'font-weight': 'bold', 'font-size': '15px' }),
    ]),
    html.Div(id='tabs-content-example-graph'),
    Footer()
])

@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.H5('Green Growth index 2021'),
           html.Div(
                            [
                                html.H5(f"Highlights"),
                                html.Br([]),
                                html.P(
                                    "Green Growth Index 2021: measures country performance in achieving sustainability targets including Sustainable Development Goals, Paris Climate Agreement, and Aichi Biodiversity Targets for four green growth dimensions: efficient and sustainable resource use, natural capital protection, green economic opportunities and social inclusion from january to December 2020.",
                                    style={"color": "#ffffff", 'font-size': '15px'},
                                    className="row",
                                ),
                                html.A("Click here to navigate 2021 Index", href="https://ggindex2021.herokuapp.com/",target ="_blanck",
                                style={"color":"black", 'font-weight': 'bold', 'font-size': '15px' } ), 
                                
                            ],
                            className="product",
                        ),
            html.H5('Green Growth index 2020'),
           html.Div(
                            [
                                html.H5(f"Highlights"),
                                html.Br([]),
                                html.P(
                                    "Green Growth Index 2020: measures country performance in achieving sustainability targets including Sustainable Development Goals, Paris Climate Agreement, and Aichi Biodiversity Targets for four green growth dimensions: efficient and sustainable resource use, natural capital protection, green economic opportunities and social inclusion from january to December 2019.",
                                    style={"color": "#ffffff", 'font-size': '15px'},
                                    className="row",
                                ),
                                html.A("Click here to navigate 2020 Index", href="https://ggindex2020.herokuapp.com/",target ="_blanck",
                                style={"color":"black", 'font-weight': 'bold', 'font-size': '15px' } ), 
                            ],
                            className="product",
                        )
        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.H3('Green-Blue Growth Index'),
            html.Div(
                            [
                                html.H5(f"Highlights"),
                                html.Br([]),
                                html.P(
                                    "Green-Blue Growth Index measures country performance in achieving sustainability targets for green and blue indicators which are relevant to achieve Sustainable Development Goals, Paris Climate Agreement, and Aichi Biodiversity Targets for four green growth dimensions: efficient and sustainable resource use, natural capital protection, green economic opportunities and social inclusion. It is developed through collaboration between GGGI and OECS Commission. (Note: Landlocked countries are not included in the Index.",
                                    style={"color": "#ffffff", 'font-size': '15px'},
                                    className="row",
                                ),
                                html.A("Click here to navigate Green-Blue Growth Index", href="https://greenblueindex.herokuapp.com/",target ="_blanck",
                                style={"color":"black", 'font-weight': 'bold', 'font-size': '15px' } ), 
                            ],
                            className="product",
                        )
        ])

    else:
        return html.Div([
            html.H3(''),
            html.Div(
                            [
                                html.H5(f""),
                                html.Br([]),
                                html.P(
                                   # "Global for the Green Growth Index are provided for countries within five geographic regions – Africa, the Americas, Asia, Europe, and Oceania. Although the trends differ across regions for the four green growth dimensions, green economic opportunities is consistently below targets and largely stable across time, except in Europe where the trend is rising slightly and greater than other regions. Another positive trend to note is that across all regions, social inclusion scores have risen systematically over the past 15 years. This is especially true in areas with many developing countries like Asia and Africa.",
                                    #style={"color": "#ffffff", 'font-size': '15px'},
                                    #className="row",
                                ),
                            ],
                            className="product",
                        )
        ])
