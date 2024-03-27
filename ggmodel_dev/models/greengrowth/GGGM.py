from ggmodel_dev.graphmodel import merge_models
from ggmodel_dev.utils import get_model_properties
from ggmodel_dev.models.Energy import Energy , Installed , Intensity
from ggmodel_dev.models.landuse  import BE2, BIOGAS, BIOMASS, NUTRIENT

from ggmodel_dev.models.water_model import EW_hungary


def flatten_dictionary(dictionary):
    
    flat_dictionary = {}
    
    for dict_name, dict in dictionary.items():
        flat_dictionary.update({k: v for k, v in dict.items()})
        
    return flat_dictionary

    

def merge_model_dictionary():
    '''To improve'''
    model_dictionary = {}
    
    model_dictionary['Energy'] = Energy.model_dictionnary
    model_dictionary['Installed'] = Installed.model_dictionnary
    model_dictionary['Intensity'] = Intensity.model_dictionnary
    
    # land use model
    model_dictionary['BE2_model'] = BE2.model_dictionnary
    model_dictionary['BIOGAS'] = BIOGAS.model_dictionnary
    model_dictionary['BIOMASS'] = BIOMASS.model_dictionnary
    model_dictionary['NUTRIENT'] = NUTRIENT.model_dictionnary
    
    # HUNGARY WATER
    model_dictionary['EW_hungary'] = EW_hungary.model_dictionnary
    
    return flatten_dictionary(model_dictionary)


def merge_model_properties():
    '''To improve'''
    model_properties = {}
    model_properties['Energy'] = Energy.model_properties
    model_properties['Installed'] = Installed.model_properties
    model_properties['Intensity'] = Intensity.model_properties
    
    # land use model
    model_properties['BE2_model'] = BE2.model_properties
    model_properties['BIOGAS'] = BIOGAS.model_properties
    model_properties['NUTRIENT'] = NUTRIENT.model_properties
    model_properties['BIOMASS'] = BIOMASS.model_properties
    
    
    # HUNGARY WATER
    model_properties['EW_hungary'] = EW_hungary.model_properties
    
    
    return flatten_dictionary(model_properties)

all_model_dictionary = merge_model_dictionary()
all_model_properties = merge_model_properties()


GreenGrowthModel = merge_models([model for _,model in all_model_dictionary.items()])

model_dictionnary = {'GGGM_model': GreenGrowthModel}

model_properties = get_model_properties('models/greengrowth/GGGM_properties.json')

all_model_dictionary.update(model_dictionnary)
all_model_properties.update(model_properties)