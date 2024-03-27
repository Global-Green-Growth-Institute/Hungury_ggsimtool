from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties
import numpy as np

TotalPES_node = {'Coal': {'type': 'input', 'unit': 'PJ', 'name': 'Coal'}, #combine models together to avoid concantination
                   'Oil': {'type': 'input', 'unit': 'PJ', 'name':'Oil'},
                   'Natural_Gas': {'type': 'input',
                      'unit':  'PJ',
                      'name': 'Natural Gas'
                      },
                   'Nuclear':{'type': 'input',
                      'unit':  'PJ',
                      'name': 'Nuclear'
                      },
                   'Renewables_intensity': {'type': 'input',
                      'unit':  'PJ',
                      'name': 'Renewables'
                      },
                   'Electricity_import': {'type': 'input',
                          'unit':  'PJ',
                      'name': 'Electricity Import'
                      },
                   'TotalPES': {'type': 'output',
                      'unit': 'PJ',
                      'name': 'Total Primary Energy Suply',
                      'computation': lambda Coal,Oil, Natural_Gas,Nuclear,Renewables_intensity,Electricity_import,**kwargs: Coal+Oil+Natural_Gas+Nuclear+Renewables_intensity+Electricity_import
                         },
                  }
TotalRGDP_node={'Trgdp': {'type': 'input', 'unit': 'LCU', 'name': 'Total Real GDP'}, 
               
                  }
           
EnergyI_node={'TotalPES': {'type': 'input', 'unit': 'PJ', 'name': 'Total Primary Energy Suply'},
                'Trgdp': {'type': 'input','unit': 'LCU','name': 'Total Real GDP'},
                'EnergyI': {'type': 'output',
                      'unit': ' (TPES[TJ] / GDP [Real million LCU])',
                      'name': 'Energy intensity (TPES [TJ] /Real million LCU) ',
                      'computation': lambda TotalPES,Trgdp,**kwargs: (TotalPES/(Trgdp/1000))
                         
                  }
               }

TotalPES_model = GraphModel(TotalPES_node)
TotalRGDP_model = GraphModel(TotalRGDP_node)
EnergyI_model = GraphModel(EnergyI_node)

Intensity_model = GraphModel(concatenate_graph_specs(
    [TotalPES_node, TotalRGDP_node,EnergyI_node]))

# Dictionnary for easier access in the interface
model_dictionnary = {
                     'Total Primary Energy Suply': TotalPES_model ,
                     'Total Real GDP': TotalRGDP_model ,
                     'Energy intensity (TPES [TJ] /Real million LCU)':EnergyI_model ,
                     'Intensity_model':Intensity_model,
                     }
model_properties = get_model_properties('models/Energy/Intensity_properties.json')