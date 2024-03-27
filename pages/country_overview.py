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
            Header(app, 'Country Overview'),

        ]),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Highlights"),
                                html.Br([]),
                                html.P("In applying the Green Growth Simulation Tool for the SDG co-benefits assessment of selected policy interventions in the Hungary National Clean Development Strategy (NCDS), the systems include energy, land, water, and waste sectors.",
                                       style={"color": "#ffffff", 'font-size': '15px'},),
                                html.Br([]),
                                html.P("Hungary is a landlocked country in Central Europe. Its capital, Budapest, is bisected by the Danube River. Its cityscape is studded with architectural landmarks from Buda’s medieval Castle Hill and grand neoclassical buildings along Pest’s Andrássy Avenue to the 19th-century Chain Bridge. Turkish and Roman influence on Hungarian culture includes the popularity of mineral spas, including at thermal Lake Hévíz.",
                                       style={"color": "#ffffff", 'font-size': '15px'}),

                                       
                            ],
                            className="product",
                        )
                    ],
                    className="pretty_container four columns",
                ),
                html.Div(
                    [
                        html.H5("Summary of results:"),
                                html.Br([]),
                                html.P("The Global Green Growth Institute (GGGI) develops and applies robust models to support its Member Countries’ decision-making and prudent planning in the context of carbon neutrality. In the National Clean Development Strategy (NCDS) that informs about Hungary’s national climate neutrality commitment, GGGI has delivered various low-carbon scenarios, such as the late action (LA) and early action (EA) climate neutrality scenarios. Based on these scenarios, significant climate action’s positive impacts on the GDP and green jobs have been reported in the NCDS.The analysis was extended to assess co-benefits on selected Sustainable Development Goals (SDG) indicators by using the Green Growth Index Simulation Tool (GGSim) (Figure 1), focusing on transport-related policy measures under Hungary’s NCDS. The result highlights of this assessment are provided below.",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Br([]),
                                #html.P("Figure 1 Framework for the GGSim tool",
                                       #style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo111.png", className='content-img'),
                                html.H5("1. Energy and transport"),
                                html.P("The policies on energy for Hungary drastically increase the renewable energy capacity in the country in the early action (EA) scenario. In addition to the increase in various renewable energy capacities, there are determined policies on increasing energy efficiency in all the sectors in the EA scenario compared with the BAU scenario. Figure 2 shows that on SDG 12.a.1, there will be an increase from 148 watts per capita to 1,210 watts per capita. At the same time, the EA scenario will witness a rise of up to 6,763 watts per capita. Regarding the trend in energy intensity, with further new policy additions in the BAU scenario, energy efficiencies in the end-use sectors will stay the same compared to the EA. Decoupling energy consumption from economic growth can help simultaneously achieve economic and environmental goals. The decoupling may result from reducing the demand for energy services (e.g., heating, lighting, and passenger or freight transport) by using energy in a more efficient way (thereby using less energy per unit of economic output) or a combination of the two. Thus, there will be more improvement in energy intensity in the EA scenario compared to the BAU.",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo222.png", className='content-img'),
                                html.P("Figure 3 shows the trend in emission reduction in the transport sector. The policies for the transport sector in the BAU scenario remain unchanged, with oil and LPG dominating the sector. There is a minimal increase in the number of electric vehicles. While in the EA scenario, electric and petrol vehicles, followed by biofuel and hydrogen vehicles, will dominate the sector. The interference of green fuels will reduce the emissions between 2020 and 2050 in the EA scenario compared to the BAU. Figure 2 also describes the land use change emission because of installing solar PV systems on forest land. In the EA scenario, with the installation of a large capacity of ground-mounted utility-scale PV, the year 2050 will significantly increase emissions.",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo333.png", className='content-img'),
                                html.P("Figure 4 shows the total land required for installing the PV systems in the BAU and EA scenarios. Due to the installation of 51 GW of PV in the EA scenario in 2050, the land required to accommodate the PV will increase correspondingly. Similarly, the increase in biofuel demand in the transport sector will increase cropland demand for crops dedicated to fulfilling the biofuel demand. As previously mentioned, the EA scenario will witness an increase in biofuel for the transport sector. However, the BAU scenario will show little increase as LPG and oil contribute to a significant share in the transport sector.",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo444.png", className='content-img'),
                                html.H5("2. Agriculture and forest"),
                                html.P("Due to the policies on biogas production from animal manure, the EA scenario shows an increase in the potential biogas production compared to the BAU (Figure 5). The use of animal manure to produce biogas will increase performance on SDG 15.3.1. (i.e., nutrient balance). The EA scenario shows a decrease in the nutrient balance caused by decreasing manure application rates and a reduction in manure left on pastureland.",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo555.png", className='content-img'),
                                html.P("The potential bioenergy production from crop residues will also increase in the EA scenario compared to BAU (Figure 6). This results from the increased crop residue removals, making the crop residues available for biofuel production. Also, in the BAU scenario, there will be a slight increase in the total bioenergy potential from crop residues as the total agricultural production will increase. Due to the removal of residues used for bioethanol production, the total emissions from crop residues will decrease compared to BAU.",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo666.png", className='content-img'),
                                html.P("The total share of forest area will increase in the EA scenario due to reforestation policies and increased agricultural productivity, which will decrease the land required for crops (Figure 7Figure 6). Above-ground biomass will increase because of wood removal policies and forest area changes.",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo777.png", className='content-img'),
                                html.P("SDG 13.3.2, total non-CO2 emissions in agriculture per capita, will decrease in the EA scenario and increase in the BAU (Figure 8). The combined set of model drivers and policies on manure, residue removals, reforestation, and food loss/waste reduction will lead to lower total emissions in the agricultural sector. These policies need to be implemented so the emissions per capita will stay the same.",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo88.png", className='content-img'),
                                html.H5("3. Water and waste"),
                                html.P("The result on water use efficiency (SDG 6.4.1) in Figure 9 shows no significant difference in this SDG indicator between the BAU and EA scenarios from 2020 to 2040. The decline in water use efficiency is attributed to the increase in industrial water withdrawals in 2030 because of increased nuclear capacity. When considering the agricultural and municipal water use efficiency, the results show an increasing trend for both sectors until 2050. SDG 6.4.2, the level of water stress, shows that, overall, Hungary will still be classified as ‘not under stress’ in the BAU and EA scenarios from 2020 and 2050. Neither scenario reaches the threshold level of 25 percent under the United Nations guidelines (FAO & UN-Water 2021b). The BAU scenario shows relatively better results compared to the EA scenario. This indicates that demand-based water management interventions and reducing fossil-fuel-based electricity generation could help to improve progress in achieving the target for SDG 6.4.2.",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo99.png", className='content-img'),
                                html.P("Under the BAU scenario, due to the relatively high connection to sanitation infrastructure and wastewater treatment facilities, Hungary has a strong performance in SDG 6.3.1 with 80 percent of safely treated domestic wastewater (Figure 10). Under the EA scenario, where the connection to tertiary wastewater treatment was improved by aligning with the new EU directive (1868/2020), this SDG indicator could be further improved to 88 percent by 2050. The increase in safely treated wastewater will also improve freshwater availability (SDG 6.4.2).",
                                       style={"color": "##000000", 'font-size': '16px'},),
                                html.Img(src="../assets/photo1010.png", className='content-img'),


                                




                                

                        #html.H6(
                           # f"2005-{INDEX_YEAR} Green Growth Index Map",
                            #className="subtitle padded",
                        #),
                        #dcc.Graph(figure=Map(data), id='world_map',
                                  #config=map_dcc_config('GGI_world_map')),
                       # html.H6(
                           # f"{INDEX_YEAR} Green Growth Index Table",
                           # className="subtitle padded",
                        #),
                        #Table(data),
                       # html.Img(src="../assets/zamb.jpg", className='img-slide'),
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
    Output("index-table1", "style_data_conditional"),
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
