from ggmodel_dev.graphmodel import GraphModel, concatenate_graph_specs
from ggmodel_dev.utils import get_model_properties
import numpy as np
#test comment  

Installed_nodes = {'PGC_Biomass': {'type': 'input', 'unit': 'megawatts', 'name': 'Biomass'}, #Electrical generation from renewables 
             'PGC_Waste': {'type': 'input', 'unit': 'megawatt', 'name': 'Waste genaration'},
              
             'PGC_Wind_on': {'type': 'input',
                      'unit':  'megawatts',
                      'name': 'Wind onshore'
                      },
            'PGC_Wind_of': {'type': 'input',
                      'unit':  'megawatts',
                      'name': 'Wind ofshore'
                      },
            'PGC_Solar_large': {'type': 'input',
                      'unit':  'megawatts',
                      'name': 'Solar large scare'
                      },
            'PGC_Solar_small': {'type': 'input',
                      'unit':  'megawatts',
                      'name': 'Solar small scare'
                      },
                   
            'PGC_Hydro_large': {'type': 'input',
                      'unit':  'megawatts',
                      'name': 'Hydropower large scare'
                      },
            'PGC_Hydro_small': {'type': 'input',
                      'unit':  'megawatts',
                      'name': 'Hydropower small scare'
                      },
                   
            'PGC_Geothermal': {'type': 'input',
                      'unit':  'megawatts',

                      'name': 'Geothermal'
                      },
               
            
           'InstalledMW': {'type': 'output',
                      'unit': 'megawatts',
                      'name': 'Installed renewable energy capacity',
                      'computation': lambda PGC_Biomass,PGC_Waste, PGC_Wind_on,PGC_Wind_of,PGC_Solar_large,PGC_Solar_small,PGC_Hydro_large,PGC_Hydro_small,PGC_Geothermal,**kwargs: PGC_Biomass+PGC_Waste+PGC_Wind_on+PGC_Wind_of+PGC_Solar_large+PGC_Solar_small+PGC_Hydro_large+PGC_Hydro_small+PGC_Geothermal
                         
                  },
           'Population': {'type': 'input',
                      'unit':  'person',
                      'name': 'Population'
                      },
          'Installedwatts': {'type': 'output',
                      'unit': 'watts per capita',
                      'name': 'Installed renewable energy capacity',
                      'computation': lambda InstalledMW,Population, **kwargs: ((InstalledMW*1000000)/Population)
                         
                  }
              
                        }
Installed_model = GraphModel(Installed_nodes) 


# Dictionnary for easier access in the interface
model_dictionnary = {'Installed_model': Installed_model}

model_properties = get_model_properties('models/Energy/Installed_properties.json')