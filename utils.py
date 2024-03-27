import dash
import dash_html_components as html
import dash_core_components as dcc


def Header(app, active_tab='Country Overview'):
    top_header = get_header(app)
    menu = get_menu(active_tab)

    page_title = html.Div(
        [
            html.Div([
                page_menu(active_tab)],
                className='twelve columns'),
        ],
        className="row")

    return html.Div([
        html.Div([
            top_header,
            html.Br([]),
            menu,
            ], className='mainheader'),
        page_title])

def MyHeader(app, active_tab='Country Overview'):
    top_header = get_header(app)
 
    return html.Div([
        html.Div([
            top_header,
             #html.H3('Green Growth index projects ' ,style={'color':'white'}),
            html.Br([]),
            ], className='mainheader'),])



def Footer():
    return html.Footer('© Global Green Growth Institute 2024. All Rights Reserved.',style={'display': 'flex', 'justify-content': 'center','fontFamily': 'Arial, sans-serif', 'fontSize': '16px'})

def get_header(app):
    header = html.Div(
        [
            html.Div(
                [   
                    html.Img(
                            src=app.get_asset_url("GGGI_logo.png"),
                            className="logo",
                            ),
                    html.Img(
                            src=app.get_asset_url("Abonyi.png"),
                            className="logo1",
                            ),
                    
                    
                    html.Div([
                        
                        #html.Ul([
                            #html.Li(
                                #[html.A("Home", href="https://greengrowthindex.gggi.org/",), ]),
                            #html.Li([html.Span(), ]),
                           # html.Li(
                                #[html.A("Index and Simulation", href="https://gggi-simtool-demo.herokuapp.com/",), ]),
                            #html.Li([html.Span(), ]),
                            #html.Li(
                               # [html.A("Projects", href="/projects",), ]),
                            #html.Li([html.Span(), ]),
                            #html.Li(
                                #[html.A("Publications", href="https://greengrowthindex.gggi.org/?page_id=3126",), ]),
                            #html.Li([html.Span(), ]),
                            #html.Li(
                               # [html.A("Authors", href="https://greengrowthindex.gggi.org/?page_id=3080",), ]),
                            #html.Li([html.Span(), ]),
                            #html.Li(
                                #[html.A("Reviewers", href="https://greengrowthindex.gggi.org/?page_id=1975",), ]),
                            #html.Li([html.Span(), ]),
                            #html.Li(
                               # [html.A("Partners", href="https://greengrowthindex.gggi.org/?page_id=2166",), ]),
                            #html.Li([html.Span(), ]),
                            #html.Li(
                               # [html.A("Contact Us", href="https://greengrowthindex.gggi.org/?page_id=2839",), ]),
                        #]),
                    ], className="mainnav"),
                ],className="twelve columns",
            ),
        ],
    )
    return header


def get_page_title(active_tab):
    pass


def get_menu_old(active_tab):

    name_link_list = [
       {'label': 'Hungary Simulation Tool','value': '/SimulationDashBoard/country_overview'},
       {'label': 'Evidence Library', 'value': '/SimulationDashBoard/models'},
    ]

    div_list = get_menu_div_list(name_link_list, active_tab=active_tab, active_style={
                                 'text-decoration': 'none', 'color': '#2db29b'}, className="tab")

    menu = html.Div(div_list, className="row all-tabs")
    return menu


def get_menu(active_tab):

    tab_menu = {
        'Country Overview': "Hungary Simulation Tool",
        'Sytem Dynamic Models': "Hungary Simulation Tool",
        'Network Analysis': "Hungary Simulation Tool",
        'ShapNet' : "Hungary Simulation Tool",
        'Correlational Analysis' : "Hungary Simulation Tool",
        'Experts': "Hungary Simulation Tool",
        'Data': "Evidence Library",
        'Models': "Evidence Library",
        'Codes': "Evidence Library",
        'Downloads': "Evidence Library",
    }

    tabs_links = {
        #'Green Growth Index': '/SimulationDashBoard/global_overview',
        'Hungary Simulation Tool': '/SimulationDashBoard/country_overview',
        'Evidence Library': '/SimulationDashBoard/models',
        #'Experts': '/SimulationDashBoard/models',
    }

    menu_list = []
    
    for name, link in tabs_links.items():
        if name == tab_menu[active_tab]:
            tab = dcc.Link(
                name,
                href=link,
                className="tab",
                style={'color': '#FFFFFF', 'font-weight': 'bold'}

            )
        else:
            tab = dcc.Link(
                name,
                href=link,
                className="tab",
            )
    
        menu_list.append(tab)

    menu = html.Div(menu_list, className="row all-tabs")
    return menu

def page_menu(active_tab):
    if active_tab in ['Country Overview','Sytem Dynamic Models','Network Analysis','ShapNet', 'Correlational Analysis','Experts']:
        return simtool_menu(active_tab)
    if active_tab in ['Models',  'Codes', 'Downloads']:
        return evidence_lib_menu(active_tab)


def simtool_menu(active_tab):
    name_link_list = [
        {'label': 'Country Overview', 'value': '/SimulationDashBoard/country_overview'},
        {'label': 'Sytem Dynamic Models', 'value': '/SimulationDashBoard/system-dynamic-models'},
        {'label': 'Network Analysis', 'value': '/SimulationDashBoard/Network-Analysis'},
        {'label': 'ShapNet', 'value': '/SimulationDashBoard/ShapNet'},
        {'label': 'Correlational Analysis', 'value': '/SimulationDashBoard/CorrelationalAnalysis'},
        {'label': 'Experts', 'value': '/SimulationDashBoard/Experts'},
    ]
    div_list = get_menu_div_list(name_link_list, active_tab, className='tab')

    return html.Div(div_list, className="row all-tabs")

def evidence_lib_menu(active_tab):
    name_link_list = [
        {'label': 'Models', 'value': '/SimulationDashBoard/models'},
        #{'label': 'Data', 'value': '/SimulationDashBoard/data'},
        {'label': 'Codes', 'value': '/SimulationDashBoard/codes'},
        {'label': 'Downloads', 'value': '/SimulationDashBoard/downloads'},
    ]
    div_list = get_menu_div_list(name_link_list, active_tab,  className='tab')
    return html.Div(div_list, className="row all-tabs")


def get_menu_div_list(name_link_list, active_tab, className='thirdtabs', active_style={'background-color': '#0bb89c', 'color': 'white'}):
    div_list = []

    for name_link in name_link_list:
        name = name_link['label']
        link = name_link['value']

        if name == active_tab:
            div = html.Div(
                [dcc.Link(html.Button(name, style=active_style), href=link)], className=className)

        else:
            div = html.Div(
                [dcc.Link(html.Button(name), href=link)], className=className)

        div_list.append(div)

    return div_list


def is_btn_clicked(btn_id):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    return btn_id in changed_id


def dcc_config(file_name):
    return {'toImageButtonOptions': {'format': 'png',
                                     'filename': f'{file_name}',
                                     'scale': 2,
                                     },
            'displaylogo': False,
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d',
                                       'select2d', 'lasso2d',
                                       'zoomIn2d', 'zoomOut2d', 'toggleSpikelines', 'autoScale2d']}