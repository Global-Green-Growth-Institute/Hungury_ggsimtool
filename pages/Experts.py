import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from utils import Header,Footer
#from utils import Header
import dash
from dash.dependencies import Input, Output
from app import app, data, INDEX_YEAR

layout = html.Div(
    [
        html.Div([
            Header(app, 'Experts'),

        ]),
        html.Div(
            [
                html.Div([html.H5("Experts:",className='expert-title')], className='expert-ti'),
                html.Div([
                    html.Div(
                    [
                        html.Div([
                            
                        html.Img(src="../assets/Lilibeth photo_v2.png", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Dr. Lilibeth A. Acosta  ",className='expert-name'),
                        html.H6("Deputy Director ",className='content1'),
                        html.H6("Program Manager ",className='content1'),
                        html.H6("Green Growth Performance Measurement(GGPM) ",className='content1'),
                        html.H6("Global Green Growth Institute    ",className='content5'),
                        html.H6(" European Office, Budapest, Hungary",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("lilibeth.acosta@gggi.org:",href="mailto:lilibeth.acosta@gggi.org",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                html.Div(
                    [
                        html.Div([
                        html.Img(src="../assets/Innocent.jpg", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Mr. Innocent Nzimenyera",className='expert-name'),
                        html.H6("Data Analyst and Python Programmer ",className='content1'),
                        html.H6("GGPM Consultant",className='content1'),
                        html.H6("Global Green Growth Institute",className='content2'),
                        html.H6("Kigali, Rwanda",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("innocent.nzimenyera@gggi.org",href="mailto:innocent.nzimenyera@gggi.org",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                html.Div(
                    [
                        html.Div([
                         html.Img(src="../assets/Ruben_WebsitePhoto.jpg", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Mr. Ruben Sabado,Jr",className='expert-name'),
                         html.H6("Data Analyst and workshop coordinator",className='content1'),
                        html.H6("GGPM Consultant",className='content2'),
                        html.H6("Global Green Growth Institute",className='content2'),
                        html.H6("Manila,Philippines",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("ruben.jr@gggi.org",href="mailto:ruben.jr@gggi.org",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                html.Div(
                    [
                        html.Div([
                          html.Img(src="../assets/Ribeus.jpeg", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Mr. Ribeus Mihigo Munezero",className='expert-name'),
                        html.H6("Data Analyst and Python Programmer ",className='content1'),
                        html.H6("GGPM Consultant",className='content1'),
                        html.H6("Global Green Growth Institute",className='content2'),
                        html.H6("Kigali, Rwanda",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("munezero.ribeus@gggi.org",href="mailto:munezero.ribeus@gggi.org",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                  html.Div(
                    [
                        html.Div([
                        html.Img(src="../assets/HermenLuchtenbelt_picture.jpg", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Mr. Hermen Luchtenbelt",className='expert-name'),
                        html.H6("Consultant, Green Growth ",className='content1'),
                        html.H6("Performance Measurement ",className='content2'),
                        html.H6("Global Green Growth Insititute",className='content2'),
                        html.H6("Amsterdam,Netherlands",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("hermenluchtenbelt@hotmail.com",href="mailto:hermenluchtenbelt@hotmail.com",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                 html.Div(
                    [
                        html.Div([
                        html.Img(src="../assets/20180822_125438.jpg", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Ms. Sanga Lee",className='expert-name'),
                        html.H6("Consultant, Green Growth ",className='content1'),
                        html.H6("Performance Measurement ",className='content2'),
                        html.H6("Global Green Growth Insititute",className='content2'),
                        html.H6("Seoul,Republic of Korea",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("ilboo2003@gmail.com",href="mailto:ilboo2003@gmail.com",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                html.Div(
                    [
                        html.Div([
                        html.Img(src="../assets/Adam_india.jpg", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Mr. Godwin Paul Adams",className='expert-name'),
                        html.H6("Consultant, Green Growth ",className='content1'),
                        html.H6("Performance Measurement ",className='content2'),
                        html.H6("Global Green Growth Insititute",className='content2'),
                        html.H6("New Delhi,India",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("adamssekar96@gmail.com",href="mailto:adamssekar96@gmail.com",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                html.Div(
                    [
                        html.Div([
                        html.Img(src="../assets/jonas1.jpg", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Dr. János Abonyi",className='expert-name'),
                        html.H6("Professor",className='content1'),
                        html.H6("HUN-REN-PE Complex Systems Monitoring Research Group",className='content1'),
                        html.H6("University of Pannonia",className='content2'),
                        html.H6("Veszprém, Hungary",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("janos@abonyilab.com",href="mailto: janos@abonyilab.com",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                
                html.Div(
                    [
                        html.Div([
                        html.Img(src="../assets/vikta.jpg", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Dr. Viktor Sebestyén",className='expert-name'),
                        html.H6("Professor",className='content1'),
                        html.H6("University of Pannonia",className='content2'),
                        html.H6("Veszprém, Hungary",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("sebestyen.viktor88@gmail.com",href="mailto: sebestyen.viktor88@gmail.com",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                html.Div(
                    [
                        html.Div([
                        html.Img(src="../assets/Timea_Czvetko.jpg", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Ms. Timea Czvetko",className='expert-name'),
                        html.H6("Consultant, Green Growth ",className='content1'),
                        html.H6("Performance Measurement ",className='content2'),
                        html.H6("Veszprém, Hungary",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("czvetko.tim@gmail.com",href="mailto:  czvetko.tim@gmail.com",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
                html.Div(
                    [
                        html.Div([
                        html.Img(src="../assets/prof_adam.png", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Mr. Ádám Ipkovich",className='expert-name'),
                        html.H6("Intern, Green Growth ",className='content1'),
                        html.H6("Performance Measurement ",className='content2'),
                        html.H6("Veszprém, Hungary",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("ipkovichadam@gmail.com",href="mailto: ipkovichadam@gmail.com",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),
            html.Div(
                    [
                        html.Div([
                        html.Img(src="../assets/Julia.png", className='img-slide'),
                        ], className='aside'),
                        html.Div([
                        html.H5("Ms. Julia Joveneau",className='expert-name'),
                        html.H6("Analyst, Green Growth ",className='content1'),
                        html.H6("Performance Measurement ",className='content2'),
                        html.H6(" European Office, Budapest, Hungary",className='content6'),
                        html.H6("E-mail:",className='content7'),html.A("julia.joveneau@gggi.org",href="mailto: julia.joveneau@gggi.org",className='content8')
                        ], className='content')
                        
                        
                    ],
                    
                    className="pretty_container11 expert-conatiner"
                ),

                ], className='main-container')
                

            ],
            className="row",
        ),
        Footer(),
    ],
    className="page",
)

#@app.callback(
    #Output("index-table", "style_data_conditional"),
    #Input("index-table", "active_cell"),
#)
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
