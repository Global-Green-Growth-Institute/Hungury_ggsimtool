__Publisher__ = 'Global Green Growth Institute'
__Author__ = 'GGPM Team'
__Model_lead__='P.Godwin'
__Programmers__='I.Nzimenyera & R.Munezero'
from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties
import numpy as np

Renewables_node = {'Biomass': {'type': 'input', 'unit': 'MWh/year', 'name': 'Biomass'}, #combine models together to avoid concantination
                   'Waste': {'type': 'input', 'unit': 'MWh/year', 'name':'Waste Generation'},
                   'Wind': {'type': 'input',
                      'unit':  'MWh/year',
                      'name': 'Wind onshore'
                      },
                   'Solar':{'type': 'input',
                      'unit':  'MWh/year',
                      'name': 'Solar large scale'
                      },
                   'Hydro': {'type': 'input',
                      'unit':  'MWh/year',
                      'name': 'Hydropower large scale'
                      },
                   'Geothermal': {'type': 'input',
                      'unit':  'MWh/year',
                      'name': 'Geothermal'
                      },
                   'Renewables': {'type': 'output',
                      'unit': 'MWh/year',
                      'name': 'Electricity generated from Renewables',
                      'computation': lambda Biomass,Waste, Wind,Solar,Hydro,Geothermal,**kwargs: Biomass+Waste+Wind+Solar+Hydro+Geothermal
                         },
                  }
all_nodes={'Renewables': {'type': 'input', 'unit': 'MWh/year', 'name': 'Electricity generated from Renewables'}, #combine models together to avoid concanti       
            'oil': {'type': 'input',
                      'unit':  'MWh/year',
                      'name': 'Diesel and fuel oil'
                      },
              'Gas': {'type': 'input',
                      'unit':  'MWh/year',
                      'name': 'Gas turbine'
                      },
              'Coal': {'type': 'input',
                      'unit':  'MWh/year',
                      'name': 'Coal'
                      },
              'Nuclear': {'type': 'input',
                      'unit':  'MWh/year',
                      'name': 'Nuclear'
                      },
              'Total_EG': {'type':'output',
                      'unit': 'MWh/year',
                      'name': 'Total Electricity generated',
                      'computation': lambda Renewables,oil,Gas,Coal,Nuclear,**kwargs:Renewables+oil+Gas+Coal+Nuclear
                         
                  }
              
                        }
EGC_renewables={'Renewables': {'type': 'input', 'unit': 'MWh/year', 'name': 'Electricity generated from Renewables'},
                'Total_EG': {'type': 'input','unit': 'MWh/year','name': 'Total Electricity generated'},
                'Share_Renewables': {'type': 'output',
                      'unit': 'Percent',
                      'name': 'Share of renewables in final electricity generation',
                      'computation': lambda Renewables,Total_EG,**kwargs:((Renewables/Total_EG)*100)
                         
                  }
               }

Energy1_partial_model = GraphModel(Renewables_node)
Energy2_partial_model = GraphModel(all_nodes)
Energy3_partial_model = GraphModel(EGC_renewables)

Share_model = GraphModel(concatenate_graph_specs(
    [Renewables_node, all_nodes,EGC_renewables]))

# Dictionnary for easier access in the interface
model_dictionnary = {
                     'Electricity generated from Renewables (MWh/year)': Energy1_partial_model ,
                     'Total Electricity generated(MWh/year)': Energy2_partial_model ,
                     'Share of renewables in final electricity generation(%)':Energy3_partial_model ,
                     'Share_model': Share_model,
                     }
model_properties = get_model_properties('models/Energy/Energy_properties.json')