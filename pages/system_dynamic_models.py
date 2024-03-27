import dash_html_components as html
import dash_core_components as dcc
from app import app, ISO_options
from dash.dependencies import Input, Output
import dash_table
from utils import Header, is_btn_clicked, Footer
from dash.exceptions import PreventUpdate
from ggmodel_dev.utils import get_data_dict_from_folder, get_data_dict_from_folder_parquet, results_to_excel


from pages.scenario_box import (Energy_scenario_box,
                                Installed_scenario_box, 
                                Intensity_scenario_box,
                                BE2_scenario_box,
                                
                                # WATER HUNGARY
                                water_scenario_box_H,
           
           
                                )

from pages.scenario_function import (run_all_scenarios_Energy,
                                     run_all_scenarios_Installed,
                                     run_all_scenarios_Intensity,
                                     run_all_scenarios_landuse,
                                     
                                     #Water model
                                     run_all_scenarios_EW_H,
                                   
                                     )


from pages.scenario_function import model_summary_dictionnary


scenario_properties = {
    'Scenario_one': {"name": 'Scenario 1'},
    'Scenario_two': {'name': 'Scenario 2'},
    'BAU': {'name': 'Business as Usual'},
}

scenario_box_dictionnary = {
    'Share_model': Energy_scenario_box,
    'Installed_model': Installed_scenario_box,
    'Intensity_model': Intensity_scenario_box,
    
    # land use model
    'BE2_model': BE2_scenario_box,
    
    #water hungary
    'EW_model': water_scenario_box_H,
    
}

scenario_data_dictionnary = {
    'Share_model': get_data_dict_from_folder('data/sim/Energy'),
    'Installed_model': get_data_dict_from_folder('data/sim/Installed'),
    'Intensity_model': get_data_dict_from_folder('data/sim/Intensity'),
    
    
    # land use model
    'BE2_model': get_data_dict_from_folder('data/sim/landuse/BE2'),
    
    #water hungary
    'EW_model': get_data_dict_from_folder('data/sim/water'),
}

scenario_function_dictionnary = {
    'Share_model': run_all_scenarios_Energy,
    'Installed_model': run_all_scenarios_Installed,
    'Intensity_model': run_all_scenarios_Intensity,
    
    # land use model
    'BE2_model': run_all_scenarios_landuse,
    
    #water hungary
    'EW_model': run_all_scenarios_EW_H,
    
  
}


def model_selection_box():
    layout = html.Div(
        [
            html.H5(
                "Select a System",
                className="subtitle padded",
            ),
            html.Br([]),
            dcc.Dropdown(id="dropdown-simulation-model",
                         options=[
                             
                           
                            
                            #Energy
                         
                            {'label': 'Share of renewables in final electricity generation (Energy)','value': 'Share_model'},
                            {'label': 'Installed renewable energy capacity (Energy)','value': 'Installed_model'},
                            {'label': 'Energy Intensity (Energy)','value': 'Intensity_model'},

                            ## land use model
                            {'label': 'Land use change (Landuse)','value': 'BE2_model'},

                            #Water model 
                            
                            {'label': 'Efficient Water Model (Water)',
                             'value': 'EW_model'},
                            
                          
                         ],
                         value='Share_model'
                        
                         )

        ])
    return layout


def scenario_building_box():
    layout = html.Div(
        [
            html.H5(
                "Build a Scenario",
                className="subtitle padded",
            ),
            html.Br([]),
            html.Div([],
                     id="scenario_box_1",
                     className='product_A'
                     ),
            html.Div([],
                     id="scenario_box_2",
                     className='product_B'
                     ),
            html.H5(
                "Country",
                className="subtitle padded",
            ),
            html.Br([]),
            html.Div([dcc.Dropdown(id="ISO_run_results",
                                   options=[{'label': country, 'value': iso}
                                            for iso, country in ISO_options],
                                   value='HUN')],
                     style={'width': '100%',
                            'display': 'inline-block',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'font-size': '20px'}
                     ),
            html.Br([]),
            html.Br([]),
            html.Div(
                [
                    html.Button('Run', id='btn-run', n_clicks=0,
                                style={'font-size': 20,
                                       'font-weight': 'normal',
                                       'color': '#ffffff',
                                       'background': '#14ac9c',
                                       'border': '#14ac9c',
                                       }),
                    dcc.Loading(
                        id="loading-scenario",
                        children=html.Div(id='loading-output'),
                        color='#14ac9c',
                        type="dot",
                    ),
                    dcc.Loading(
                        children=html.Div(id='loading-download'),
                        color='#14ac9c',
                        type="dot",
                    ),
                    html.Button('Download Raw Data', id='btn-download', n_clicks=0,
                                style={'font-size': 15,
                                       'font-weight': 'normal',
                                       'color': '#ffffff',
                                       'background': '#14ac9c',
                                       'border': '#14ac9c',
                                       }),
                    dcc.Download(id="download-xls"),
                    html.Br([]),
                    html.H5("Required data", className="subtitle padded"),
                    html.Br([]),
                    dash_table.DataTable(id='sim-data-table',
                                 columns=[{"name": i, "id": i}
                                          for i in ['Variable','Name', 'Availability']],
                                 )

                ],
                className='row'
            ),
        ],
        className='row'
    )

    return layout


def extract_values_from_ided_component(component):
    '''Dangerous way to filter out the index'''
    return {component['props']['id'][:-4]: component['props']['value']}


def get_args_dict_from_scenario_box(box):
    '''TO DO: Recursive search of the id'''
    ided_components = [el for el in box['props']
                       ['children'] if 'id' in el['props']]

    arg_dict = {}
    for component in ided_components:
        if 'value' in component['props']:
            arg_dict.update(extract_values_from_ided_component(component))
        else:
            unested_comp = []
            # to make recursive, not sustainable as is
            for comp_1 in component['props']['children']:
                for comp_2 in comp_1['props']['children']:
                    for comp_3 in comp_2['props']['children']:
                        if 'id' in comp_3['props']:
                            unested_comp.append(comp_3)

            for el in unested_comp:
                arg_dict.update(extract_values_from_ided_component(el))

    return arg_dict

import plotly.graph_objs as go
import pandas as pd



def get_sim_tab():
    
    return html.Div(
                [
                    html.H6(
                        "Simulation Results(Hover on the point to check the Values)",
                        className="subtitle padded",
                    ),
                    html.Div(
                        [
                            dcc.Graph(id='results-graph-1',
                                    config={'displayModeBar': False}),
                            dcc.Graph(id='results-graph-2',
                                    config={'displayModeBar': False}),
                            #dcc.Graph(id='results-graph-3',
                                    #config={'displayModeBar': False}),
                        ],
                        className='row'),
                ],
            )
    

layout = html.Div(
    [
        html.Div([Header(app, 'Sytem Dynamic Models')]),
        html.Div(
            [
                model_selection_box(),
                html.Br([]),
                scenario_building_box()
            ],
            className="pretty_container four columns ",
        ),
        html.Div(
            [                
                html.Div([get_sim_tab()], id='sim-spatial-tabs-content', className='pretty_container eight columns'),
            ],
            className='row'
        ),
        Footer(),
    ],
    className="page",
)


@app.callback(
    
   # Output("index-table2", "style_data_conditional"),
   # Input("index-table1", "active_cell"),
    
    Output('scenario_box_1', 'children'),
    Output('scenario_box_2', 'children'),
    [
        Input('dropdown-simulation-model', 'value'),
    ]
)

                                                       

def update_scenario_box(model_name):
    scenario_box_function = scenario_box_dictionnary[model_name]
    return scenario_box_function(scenario_id='_one'), scenario_box_function(scenario_id='_two')


def get_spatial_tab():
    return html.Div([
        html.Div([html.H3('Not available')], className='product_A', style={'background': '#D3D3D3'}),
        html.Div([dcc.Graph(id='map', config={'displayModeBar': False}),], className='row')
        ]
    )


@app.callback(Output('sim-spatial-tabs-content', 'children'),
              Input('sim-spatial-tabs', 'value'))
def render_tab(tab):
    if tab == 'sim':
        return get_sim_tab()
    elif tab == 'spatial':
        return get_spatial_tab()


@app.callback(
    Output("results-graph-1", "figure"),
    Output("results-graph-2", "figure"),
    #Output("results-graph-3", "figure"),
    Output("loading-output", "children"),
    [
        Input('scenario_box_1', 'children'),
        Input('scenario_box_2', 'children'),
        Input('ISO_run_results', 'value'),
        Input('dropdown-simulation-model', 'value'),
        Input("btn-run", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def run_scenario(box_1, box_2, ISO, model, n_clicks):
    if is_btn_clicked('btn-run'):
        args_dict_1 = get_args_dict_from_scenario_box(box_1)
        args_dict_2 = get_args_dict_from_scenario_box(box_2)

        #print(round(time.time()*100))

        try:
            scenario_function = scenario_function_dictionnary[model]
            data = scenario_data_dictionnary[model]
            fig_1, fig_2, scenarios_results, scenario = scenario_function(
                data, ISO, args_dict_1, args_dict_2)
                

        except Exception as e:
            print(e)
            return {}, {}, {}, None

        return fig_1, fig_2, None

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise PreventUpdate


@app.callback(
    Output("download-xls", "data"),
    Output("loading-download", "children"),
    [
        Input('scenario_box_1', 'children'),
        Input('scenario_box_2', 'children'),
        Input('ISO_run_results', 'value'),
        Input('dropdown-simulation-model', 'value'),
        Input("btn-download", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def downdload_table(box_1, box_2, ISO, model, n_clicks):
    if is_btn_clicked('btn-download'):
        args_dict_1 = get_args_dict_from_scenario_box(box_1)
        args_dict_2 = get_args_dict_from_scenario_box(box_2)

        #print(round(time.time()*100))

        try:
            scenario_function = scenario_function_dictionnary[model]
            data = scenario_data_dictionnary[model]
            fig_1, fig_2, scenarios_results, scenario = scenario_function(
                data, ISO, args_dict_1, args_dict_2)

            results_to_excel(scenarios_results, scenario.MODEL, 'outputs/simulation_results.xlsx')

        except Exception as e:
            print(e)
            return None, None

        return dcc.send_file(f'outputs/simulation_results.xlsx'), None

    else:  # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/8
        raise PreventUpdate



# might be helpful to generalize this for any variable
@app.callback(
    Output("IRRTECH_sprinkler_one", "value"),
    Output("IRRTECH_surface_one", "value"),
    Output("IRRTECH_drip_one", "value"),
    Output("IRRTECH_sprinkler_two", "value"),
    Output("IRRTECH_surface_two", "value"),
    Output("IRRTECH_drip_two", "value"),
    [
        Input('ISO_run_results', 'value'),
        Input('dropdown-simulation-model', 'value'),
    ],
)
def update_Energy_display(ISO, model):
    if model == 'Share_model':
        data = (scenario_data_dictionnary['Share_model']['Biomass'] * 100).round(1)
        #sprinkler = data.loc[ISO, 2017, 'Sprinkler']
        #surface = data.loc[ISO, 2017, 'Surface']
        #drip =  data.loc[ISO, 2017, 'Drip']
        #return sprinkler, surface, drip, sprinkler, surface, drip


import pandas as pd

def get_availibility_table(ISO, data_dict, summary_df):
    table = pd.DataFrame.from_dict({k: ISO in s for k,s in data_dict.items() if 'ISO' in s.index.names}, orient='index').rename(columns={0: 'Available'})
    table = table.merge(summary_df, left_index=True, right_index=True).query('type in ["parameter", "input"]')[['Available', 'name']].reset_index().rename(columns={'name': 'Name', 'Available': 'Availability', 'index': 'Variable'})
    return table.sort_values(by='Name')


@app.callback(
    Output("sim-data-table", "data"),
    Output('btn-run', 'style'),
    Output('btn-download', 'style'),

    [
        Input('ISO_run_results', 'value'),
        Input('dropdown-simulation-model', 'value'),
    ],
)
def update_availibility_tab(ISO, model):
    summary_df = model_summary_dictionnary[model]
    data = scenario_data_dictionnary[model]

    table = get_availibility_table(ISO, data, summary_df)

    available = table['Availability'].sum() == table.shape[0]


    table = table.replace([True, False], ['✔️', '❌']).to_dict('records')


    if available:
        style={'font-size': 17,
            'font-weight': 'normal',
            'color': '#ffffff',
            'background': '#14ac9c',
            'border': '#14ac9c',
            }
    else:
        style={'font-size': 17,
            'font-weight': 'normal',
            'color': '#ffffff',
            'background': '#D3D3D3',
            'border': '#D3D3D3',
            }

    return table, style, style