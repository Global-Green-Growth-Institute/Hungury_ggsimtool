import pandas as pd
import plotly.express as px
from plots.simulation.GE3_plots import sankeyplot, emission_data_dict_to_df
from plots.simulation.ELEC_plots import density_map, ghg_capa_ww_plot
from plots.simulation.base_plots import scenario_line_plot, scenario_line_plot_modified, scenario_line_plot_modified_2,scenario_line_plot_modified3,scenario_line_plot_modified4,scenario_line_plot_installedMW,scenario_line_plot_installedWattspercapita,scenario_line_plot_TotalPES,scenario_line_plot_EnergyI, scenario_line_plot_water_1,scenario_line_plot_water_2


from ggmodel_dev.models.Energy import Energy_scenario,Installed_scenario,Intensity_scenario

# land use
from ggmodel_dev.models.landuse import BE2_scenario

#water model
from ggmodel_dev.models.water_model import EW_hungary_scenario

def format_var_results(scenarios_results, var):
    df = pd.concat([
        scenarios_results['scenario_one'][var].reset_index().assign(
            scenario='Scenario 1'),
        scenarios_results['scenario_two'][var].reset_index().assign(
            scenario='Scenario 2'),
        scenarios_results['BAU'][var].reset_index().assign(scenario='BAU'),
    ], axis=0).rename(columns={0: var})
    return df


model_summary_dictionnary = {
    'Share_model': Energy_scenario.MODEL.summary_df,
    'Installed_model': Installed_scenario.MODEL.summary_df,
    'Intensity_model': Intensity_scenario.MODEL.summary_df,
    
    # land use model
    
    'BE2_model': BE2_scenario.MODEL.summary_df,

    # water model
    'EW_model': EW_hungary_scenario.MODEL.summary_df,
    
}


def run_all_scenarios_Energy(data_dict, ISO, args_dict_1, args_dict_2):
    summary_df = Energy_scenario.MODEL.summary_df


    ISO_data_dict = {key: value.loc[[ISO]] for key, value in data_dict.items() }#if key not in ['Share of renewables in final electricity generation']}
    #ISO_data_dict['Share of renewables in final electricity generation'] = data_dict['Share of renewables in final electricity generation'].reset_index().set_index(['ISO'])['0'] # To do properly elswhere


    scenarios_results = Energy_scenario.run_all_scenarios(ISO_data_dict, args_dict_1, args_dict_2)

    df_1 = format_var_results(scenarios_results, 'Total_EG')
    df_2 = format_var_results(scenarios_results, 'Share_Renewables')
    #df_3 = format_var_results(scenarios_results, 'GDPC')

    fig_1 = scenario_line_plot_modified4('Total_EG', df_1, ISO, summary_df)
    fig_2 = scenario_line_plot_modified3('Share_Renewables', df_2, ISO, summary_df)
    #fig_3 = scenario_line_plot('GDPC', df_3, ISO, summary_df)

    return fig_1,fig_2,scenarios_results, Energy_scenario


def run_all_scenarios_Installed(data_dict, ISO, args_dict_1, args_dict_2):
    summary_df = Installed_scenario.MODEL.summary_df


    ISO_data_dict = {key: value.loc[[ISO]] for key, value in data_dict.items() }#if key not in ['Share of renewables in final electricity generation']}
    #ISO_data_dict['Share of renewables in final electricity generation'] = data_dict['Share of renewables in final electricity generation'].reset_index().set_index(['ISO'])['0'] # To do properly elswhere


    scenarios_results = Installed_scenario.run_all_scenarios(ISO_data_dict, args_dict_1, args_dict_2)

    df_1 = format_var_results(scenarios_results, 'InstalledMW')
    df_2 = format_var_results(scenarios_results,'Installedwatts')
    


    fig_1 = scenario_line_plot_installedMW('InstalledMW', df_1, ISO, summary_df)
    fig_2 = scenario_line_plot_installedWattspercapita('Installedwatts', df_2, ISO, summary_df)
    

    return fig_1,fig_2, scenarios_results, Installed_scenario


def run_all_scenarios_Intensity(data_dict, ISO, args_dict_1, args_dict_2):
    summary_df = Intensity_scenario.MODEL.summary_df


    ISO_data_dict = {key: value.loc[[ISO]] for key, value in data_dict.items() }#if key not in ['Share of renewables in final electricity generation']}
    #ISO_data_dict['Share of renewables in final electricity generation'] = data_dict['Share of renewables in final electricity generation'].reset_index().set_index(['ISO'])['0'] # To do properly elswhere


    scenarios_results = Intensity_scenario.run_all_scenarios(ISO_data_dict, args_dict_1, args_dict_2)

    df_1 = format_var_results(scenarios_results, 'TotalPES')
    df_2 = format_var_results(scenarios_results, 'EnergyI')
    #df_3 = format_var_results(scenarios_results, 'GDPC')

    fig_1 = scenario_line_plot_TotalPES('TotalPES',df_1,ISO, summary_df)
    fig_2 = scenario_line_plot_EnergyI('EnergyI', df_2, ISO, summary_df)
    #fig_3 = scenario_line_plot('GDPC', df_3, ISO, summary_df)

    return fig_1,fig_2,scenarios_results, Intensity_scenario



### land use model

def run_all_scenarios_landuse(data_dict, ISO, args_dict_1, args_dict_2):
    
    data_dict = {k: v.loc[ISO, 2017:] for k, v in data_dict.items()}
    
    
    scenarios_results = BE2_scenario.run_all_scenarios(data_dict, args_dict_1, args_dict_2)

    #df_1 = format_var_results(scenarios_results, 'BE2')
    #df_2 = format_var_results(scenarios_results, 'delta_CL')
    df_1 = format_var_results(scenarios_results, 'Pop')
    df_2 = format_var_results(scenarios_results, 'Pop')
    #df_3 = format_var_results(scenarios_results, 'delta_CL')

    summary_df = BE2_scenario.MODEL.summary_df

    #fig_1 = scenario_line_plot('BE2', df_1, ISO, summary_df)
    #fig_2 = scenario_line_plot('delta_CL', df_2, ISO, summary_df)
    fig_1 = scenario_line_plot_modified('Pop',df_1, ISO, summary_df)
    fig_2 = scenario_line_plot_modified_2 ('Pop',df_2, ISO, summary_df)
    #fig_3 = scenario_line_plot('delta_CL', df_3, ISO, summary_df)
    #fig_3 = scenario_line_plot('delta_CL', df_23, ISO, summary_df)

    return fig_1,fig_2,scenarios_results,BE2_scenario

# Water model

def run_all_scenarios_EW_H(data_dict, ISO, args_dict_1, args_dict_2):
    
    summary_df = EW_hungary_scenario.MODEL.summary_df


    ISO_data_dict = {key: value.loc[[ISO]] for key, value in data_dict.items() if key not in ['IRRTECHEFFi']}
    ISO_data_dict['IRRTECHEFFi'] = data_dict['IRRTECHEFFi'].reset_index().set_index(['Item'])['0'] # To do properly elswhere


    scenarios_results = EW_hungary_scenario.run_all_scenarios(ISO_data_dict, args_dict_1, args_dict_2)

    df_1 = format_var_results(scenarios_results, 'EW1')
    df_2 = format_var_results(scenarios_results, 'EW2')
    #df_3 = format_var_results(scenarios_results, 'GDPC')


    fig_1 = scenario_line_plot_water_1('EW1', df_1, ISO, summary_df)
    fig_2 = scenario_line_plot_water_2('EW2', df_2, ISO, summary_df)
    #fig_3 = scenario_line_plot('GDPC', df_3, ISO, summary_df)

    return fig_1, fig_2, scenarios_results, EW_hungary_scenario
