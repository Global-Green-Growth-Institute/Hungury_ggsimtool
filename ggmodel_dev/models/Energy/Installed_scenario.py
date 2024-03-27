from ggmodel_dev.projection import *
from ggmodel_dev.models.Energy.Installed import model_dictionnary


MODEL = model_dictionnary['Installed_model']


def run_scenario(data_dict):

    data_dict = data_dict.copy()

    scenario_projection_dict = {
        'PGC_Biomass': lambda x: x,
        'PGC_Waste': lambda x: x,
        'PGC_Wind_on': lambda x: x,
        'PGC_Wind_of': lambda x: x,
        'PGC_Solar_large': lambda x: x,
        'PGC_Solar_small': lambda x: x,
        'PGC_Hydro_large': lambda x: x,
        'PGC_Hydro_small': lambda x: x,
        'PGC_Geothermal': lambda x: x,
        'InstalledMW': lambda x: x,
        'Population': lambda x: x,
        'Installedwatts': lambda x: x

    }

    data_dict = run_projection(scenario_projection_dict, data_dict)

    results = MODEL.run(data_dict)

    return results

def run_all_scenarios(data_dict, args_dict_1, args_dict_2):
    scenarios_results = {}

    scenarios_results['BAU'] = run_scenario(data_dict=data_dict, **args_dict_1, **args_dict_2)
    scenarios_results['scenario_one'] = run_scenario(data_dict ) #, **args_dict_1)
    scenarios_results['scenario_two'] = run_scenario(data_dict) #**args_dict_2)

    return scenarios_results