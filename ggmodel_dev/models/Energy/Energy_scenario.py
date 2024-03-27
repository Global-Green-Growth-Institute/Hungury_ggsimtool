from ggmodel_dev.projection import *
from ggmodel_dev.models.Energy.Energy import model_dictionnary


MODEL = model_dictionnary['Share_model']


def run_scenario(data_dict):

    data_dict = data_dict.copy()

    scenario_projection_dict = {
        'Biomass': lambda x: x,
        'Waste': lambda x: x,
        'Wind': lambda x: x,
        'Solar': lambda x: x,
        'Hydro': lambda x: x,
        'Geothermal': lambda x: x,
        'Renewables': lambda x: x,
        'oil': lambda x: x,
        'Gas': lambda x: x,
        'Coal': lambda x: x,
        'Nuclear': lambda x: x,
        'Total_EG': lambda x: 5*x,
        'Share_Renewables': lambda x: x

    }

    data_dict = run_projection(scenario_projection_dict, data_dict)

    results = MODEL.run(data_dict)

    return results

def run_all_scenarios(data_dict, args_dict_1, args_dict_2):
    scenarios_results = {}
    scenarios_results['BAU'] = run_scenario(data_dict)
    scenarios_results['scenario_one'] = run_scenario(data_dict ) #, **args_dict_1)
    scenarios_results['scenario_two'] = run_scenario(data_dict) #**args_dict_2)


    return scenarios_results