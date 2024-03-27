from ggmodel_dev.projection import *
from ggmodel_dev.models.Energy.Intensity import model_dictionnary


MODEL = model_dictionnary['Intensity_model']


def run_scenario(data_dict):

    data_dict = data_dict.copy()

    scenario_projection_dict = {
        'Coal': lambda x: x,
        'Oil': lambda x: x,
        'Natural_Gas': lambda x: x,
        'Nuclear': lambda x: x,
        'Renewables_intensity': lambda x: x,
        'Electricity_import': lambda x: x,
        'TotalPES': lambda x: x,
        'Trgdp': lambda x: x,
        'EnergyI': lambda x: x

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