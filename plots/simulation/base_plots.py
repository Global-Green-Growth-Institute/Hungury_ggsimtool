import plotly.express as px
import pandas as pd
import os

def scenario_line_plot(var, df, ISO, summary_df):  # ugly af
    var_info = summary_df.loc[var]
    var_name = var_info['name']
    df = df.rename(columns={var: var_name})
    fig = px.line(df.query(f"ISO == '{ISO}' and Year >= 2000"),
                  x='Year',
                  y=var_name,
                  color='scenario',
                  color_discrete_map={'LA': '#D8A488',
                                      'EA': '#86BBD8',
                                      'BAU': '#A9A9A9'},
                  )

    #fig.add_vline(x=2017, line_width=3, line_dash="dash", line_color="green")
    fig.update_layout( hovermode="x",
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)'
                      ,)
    fig.update_layout(legend_title_text='Scenario')
    return fig



def scenario_line_plot_modified(var, df, ISO, summary_df):  # ugly af
    
    #print(os.getcwd())
    shareof = pd.read_csv('./data/sim/landuse/shareofforest.csv')
    
    figure={
            'data': [
                    {'x': shareof['Year'], 'y':shareof['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                    {'x': shareof['Year'], 'y':shareof['SC1'], 'name':'EA','line' :dict(color='#86BBD8',dash='line')},
                    {'x': shareof['Year'], 'y':shareof['SC2'], 'line' :dict(color='#D8A488', dash='line'),'name': u'LA'},
                   # {'x': 2017,  'line_width':3, 'line_dash':"dash", 'line_color':"green", 'name':'Baseline'},
                
                    #{'x': biomass['Year'], 'y':biomass['SC2'], 'name':'SC2',  'line' :dict(color='royalblue', width=4, dash='dash')},
                    #{'x':2017, 'type': 'vline', 'name': 'Baseline' }, #  line_dash="dash",   line_color="green")
            ],
        
        
            'layout':{
                        'title': 'Share of forest land to total land area',
                        'xaxis':{
                            'title':'Year'
                        },
                        'yaxis':{
                            'title': '[Pecent]'
                        }
            }
    }
    
    
    #figure.add_vline(x=2017, line_width=3, line_dash="dash", line_color="green")
    #figure.update_layout(hovermode="x")
    return figure
    
    
    
    
    # fig = px.line(df.query(f"ISO == '{ISO}' and Year >= 2000"),
    #               x='Year',
    #               y=var_name,
    #               color='scenario',
    #               color_discrete_map={'Scenario 1': '#D8A488',
    #                                   'Scenario 2': '#86BBD8',
    #                                   'BAU': '#A9A9A9'},
    #               )

    # fig.add_vline(x=2017, line_width=3, line_dash="dash", line_color="green")
    # fig.update_layout(hovermode="x")
    # fig.update_layout(legend_title_text='Scenario')
    # return fig


def scenario_line_plot_modified_2(var, df, ISO, summary_df):  # ugly af
    
    #print(os.getcwd())
    data = pd.read_csv('./data/sim/landuse/food_losses.csv')
    #shareof = pd.read_csv('./data/sim/landuse/shareofforest.csv')
    
    figure={
                                         'data': [
                                             {'x': data['Year'], 'y':data['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                                             {'x': data['Year'], 'y':data['EA'], 'line' :dict(color='#86BBD8',dash='line'), 'name': u'EA'},
                                             {'x': data['Year'], 'y':data['SDG Target'], 'name':'SDG Target',  'line' :dict(color='royalblue', width=4, dash='dash')},
                                             {'x':2017, 'type': 'vline', 'name': 'Baseline' }, #  line_dash="dash",   line_color="green")
                                         ],
                                    
                                    
                                     'layout':{
                                                 'title': 'Food Losses',
                                                 'xaxis':{
                                                     'title':'Year'
                                                 },
                                                 'yaxis':{
                                                     'title': 'Food Loss Index'
                                                 }
                                             }
    }
    return figure


def scenario_line_plot_modified3(var, df, ISO, summary_df):  # ugly af
    
    #print(os.getcwd())
    shareof = pd.read_csv('./data/sim/Energy/Share_Renewables.csv')
    
    figure={
            'data': [
                    {'x': shareof['Year'], 'y':shareof['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                    {'x': shareof['Year'], 'y':shareof['EA'], 'name':'EA','line' :dict(color='#86BBD8',dash='line')},
                    {'x': shareof['Year'], 'y':shareof['LA'], 'line' :dict(color='#D8A488', dash='line'),'name': u'LA'},
                   # {'x': 2017,  'line_width':3, 'line_dash':"dash", 'line_color':"green", 'name':'Baseline'},
                
                    #{'x': biomass['Year'], 'y':biomass['SC2'], 'name':'SC2',  'line' :dict(color='royalblue', width=4, dash='dash')},
                    #{'x':2017, 'type': 'vline', 'name': 'Baseline' }, #  line_dash="dash",   line_color="green")
            ],
        
        
            'layout':{
                        'title': 'Share of renewables in final electricity generation',
                        'xaxis':{
                            'title':'Year'
                        },
                        'yaxis':{
                            'title': 'Percent'
                        }
            }
    }
    
    return figure

def scenario_line_plot_modified4(var, df, ISO, summary_df):  # ugly af
    
    #print(os.getcwd())
    shareof = pd.read_csv('./data/sim/Energy/Total_EG.csv')
    
    figure={
            'data': [
                    {'x': shareof['Year'], 'y':shareof['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                    {'x': shareof['Year'], 'y':shareof['EA'], 'name':'EA','line' :dict(color='#86BBD8',dash='line')},
                    {'x': shareof['Year'], 'y':shareof['LA'], 'line' :dict(color='#D8A488', dash='line'),'name': u'LA'},
                   # {'x': 2017,  'line_width':3, 'line_dash':"dash", 'line_color':"green", 'name':'Baseline'},
                
                   #{'x': biomass['Year'], 'y':biomass['SC2'], 'name':'SC2',  'line' :dict(color='royalblue', width=4, dash='dash')},
                    #{'x':2017, 'type': 'vline', 'name': 'Baseline' }, #  line_dash="dash",   line_color="green")
            ],
        
        
            'layout':{
                        'title': 'Total electricity generated',
                        'xaxis':{
                            'title':'Year'
                        },
                        'yaxis':{
                            'title': 'MWh/year'
                        }
            }
    }
    
    return figure

def scenario_line_plot_installedMW(var, df, ISO, summary_df):  # ugly af
    
    #print(os.getcwd())
    shareof = pd.read_csv('./data/sim/Installed/InstalledMW.csv')
    
    figure={
            'data': [
                    {'x': shareof['Year'], 'y':shareof['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                    {'x': shareof['Year'], 'y':shareof['EA'], 'name':'EA','line' :dict(color='#86BBD8',dash='line')},
                    {'x': shareof['Year'], 'y':shareof['LA'], 'line' :dict(color='#D8A488', dash='line'),'name': u'LA'},
                   # {'x': 2017,  'line_width':3, 'line_dash':"dash", 'line_color':"green", 'name':'Baseline'},
                
                   #{'x': biomass['Year'], 'y':biomass['SC2'], 'name':'SC2',  'line' :dict(color='royalblue', width=4, dash='dash')},
                    #{'x':2017, 'type': 'vline', 'name': 'Baseline' }, #  line_dash="dash",   line_color="green")
            ],
        
        
            'layout':{
                        'title': 'Installed renewable energy capacity(MW)',
                        'xaxis':{
                            'title':'Year'
                        },
                        'yaxis':{
                            'title': 'MW'
                        }
            }
    }
    
    return figure

def scenario_line_plot_installedWattspercapita(var, df, ISO, summary_df):  # ugly af
    
    #print(os.getcwd())
    shareof = pd.read_csv('./data/sim/Installed/Installedwatts.csv')
    
    figure={
            'data': [
                    {'x': shareof['Year'], 'y':shareof['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                    {'x': shareof['Year'], 'y':shareof['EA'], 'name':'EA','line' :dict(color='#86BBD8',dash='line')},
                    {'x': shareof['Year'], 'y':shareof['LA'], 'line' :dict(color='#D8A488', dash='line'),'name': u'LA'},
                   # {'x': 2017,  'line_width':3, 'line_dash':"dash", 'line_color':"green", 'name':'Baseline'},
                
                   #{'x': biomass['Year'], 'y':biomass['SC2'], 'name':'SC2',  'line' :dict(color='royalblue', width=4, dash='dash')},
                    #{'x':2017, 'type': 'vline', 'name': 'Baseline' }, #  line_dash="dash",   line_color="green")
            ],
        
        
            'layout':{
                        'title': 'Installed renewable energy capacity(Watts per capita)',
                        'xaxis':{
                            'title':'Year'
                        },
                        'yaxis':{
                            'title': 'watts per capita'
                        }
            }
    }
    
    return figure

#Energy Intensity plotting 

def scenario_line_plot_TotalPES(var, df, ISO, summary_df):  # ugly af
    
    #print(os.getcwd())
    shareof = pd.read_csv('./data/sim/Intensity/TotalPES.csv')
    
    figure={
            'data': [
                    {'x': shareof['Year'], 'y':shareof['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                    {'x': shareof['Year'], 'y':shareof['EA'], 'name':'EA','line' :dict(color='#86BBD8',dash='line')},
                    #{'x': shareof['Year'], 'y':shareof['LA'], 'line' :dict(color='#D8A488', dash='line'),'name': u'LA'},
                   # {'x': 2017,  'line_width':3, 'line_dash':"dash", 'line_color':"green", 'name':'Baseline'},
                
                   #{'x': biomass['Year'], 'y':biomass['SC2'], 'name':'SC2',  'line' :dict(color='royalblue', width=4, dash='dash')},
                    #{'x':2017, 'type': 'vline', 'name': 'Baseline' }, #  line_dash="dash",   line_color="green")
            ],
        
        
            'layout':{
                        'title': 'Total Primary Energy Suply',
                        'xaxis':{
                            'title':'Year'
                        },
                        'yaxis':{
                            'title': 'PJ'
                        }
            }
    }
    
    return figure

def scenario_line_plot_EnergyI(var, df, ISO, summary_df):  # ugly af
    
    #print(os.getcwd())
    shareof = pd.read_csv('./data/sim/Intensity/EnergyI.csv')
    
    figure={
            'data': [
                    {'x': shareof['Year'], 'y':shareof['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                    {'x': shareof['Year'], 'y':shareof['EA'], 'name':'EA','line' :dict(color='#86BBD8',dash='line')},
                    #{'x': shareof['Year'], 'y':shareof['LA'], 'line' :dict(color='#D8A488', dash='line'),'name': u'LA'},
                   # {'x': 2017,  'line_width':3, 'line_dash':"dash", 'line_color':"green", 'name':'Baseline'},
                
                   #{'x': biomass['Year'], 'y':biomass['SC2'], 'name':'SC2',  'line' :dict(color='royalblue', width=4, dash='dash')},
                    #{'x':2017, 'type': 'vline', 'name': 'Baseline' }, #  line_dash="dash",   line_color="green")
            ],
        
        
            'layout':{
                        'title': 'Energy intensity (TPES [TJ] /Real million LCU)',
                        'xaxis':{
                            'title':'Year'
                        },
                        'yaxis':{
                            'title': '(TPES[TJ] / GDP [Real million LCU])'
                        }
            }
    }
    
    return figure



def scenario_line_plot_water_1(var, df, ISO, summary_df):  # ugly af
    
    #print(os.getcwd())
    shareof = pd.read_csv('./data/sim/water/EW1.csv')
    figure={
            'data': [
                    {'x': shareof['Year'], 'y':shareof['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                    {'x': shareof['Year'], 'y':shareof['EA'], 'name':'EA','line' :dict(color='#86BBD8',dash='line')},   
            ],
            'layout':{
                        'title': 'Total Water Use Efficiency (USD/m3)',
                        'xaxis':{
                            'title':'Year'
                        },
                        'yaxis':{
                            'title': 'Value (USD/m3)'
                        }
            }
    }
    
    return figure

def scenario_line_plot_water_2(var, df, ISO, summary_df):  # ugly af
    shareof = pd.read_csv('./data/sim/water/EW2.csv')
    figure={
            'data': [
                    {'x': shareof['Year'], 'y':shareof['BAU'], 'line' :dict(color='#A9A9A9',dash='line'), 'name': 'BAU' },
                    {'x': shareof['Year'], 'y':shareof['EA'], 'name':'EA','line' :dict(color='#86BBD8',dash='line')}, 
            ],        
            'layout':{
                        'title': 'Freshwater withdrawal to Freshwater Availability (%)',
                        'xaxis':{
                            'title':'Year'
                        },
                        'yaxis':{
                            'title': 'Value (Percent)'
                        }
            }
    }
    
    return figure
    
    
    
    
    
    
