"""This file includes functions to improve the handling of shapnet.py"""
import pandas as pd
import numpy as np
import shap
__author__ = "Adam Ipkovich"


def read_EW_data(address : str) -> None:
    """This function specifically read the data for the EW1 and EW2 models from the collective excel file.
    ## Args:
       - address: The address of the excel file containing the data
    ## Returns:
       - outs (dict[str, dataframe]): A dictionary of the EW1 and EW2 dataframes, containing the multiindexed time series data (variable_name : dataframe)
       - data_desc (dict[str, any]): A dictionary of the variable descriptions
       - data (dict[str, dataframe]): A dictionary of the input dataframes (variable_name : dataframe)
    """

    outs = {}
    data_desc = {}
    data = {}

    xls = pd.ExcelFile(address)
    for i in xls.sheet_names:
        ## Construct a pandas dataframe from the excel sheet!
        temp = pd.read_excel(address, engine="openpyxl", sheet_name=i, header=None)  ## read with pandas

        ## Get the variable names and descriptions -> the first 5 rows are metadata
        val_cols = temp.iloc[4, -3::].tolist()
        val_cols[0] = i
        data_desc[i] = temp.loc[0:3, 2:3].to_dict()

        ## Start building the individual dataframe
        temp = temp.drop([0, 1, 2, 3, 4]) ##
        temp.iloc[0, -3::] = val_cols
        temp.columns = temp.iloc[0, :]
        temp = temp.iloc[1:, :]
        temp.drop(columns=val_cols[-2::], inplace=True)

        ## Generally speaking, to enable scenario based evaluation, the data includes a column for the scenario name. We currently only use the fisrt "BAU" column
        ## that is not necessary the data from the simulation tool. This allows for implementing a scenario-based evlauation in the future.

        temp.reset_index(inplace=True, drop=True)

        ## Note: Can only handle ISO, Year, Item as multiindexing
        ## try catch is not necessarily a good practice.
        if "ISO" in temp.columns.to_list():
            temp.loc[:, "ISO"] = temp.loc[0, "ISO"]

        if "Year" in temp.columns.to_list():
            if temp.loc[:, "Year"].isna().any():
                try:
                    for j in range(2000, 2020):
                        temp.loc[:, "Year"] = temp.loc[:, "Year"].fillna(value=j, limit=2)

                except:
                    pass
            temp = temp.loc[temp.loc[:, "Year"] < 2020, :]

        if "Item" in temp.columns.to_list():
            if temp.loc[:, "Item"].isna().any():
                try:
                    for i in temp.loc[:, "Item"].unique():
                        if i != 'nan':
                            temp.loc[:, "Item"] = temp.loc[:, "Item"].fillna(value=i,
                                                                             limit=temp.loc[:, "Year"].unique().shape[
                                                                                       0] - 1)
                except:
                    pass

        n_ind = []
        for k in ["ISO", "Year", "Item"]:
            if k in temp.columns.to_list():
                # This is bad practice, but it works
                try:
                    n_ind.append(temp.columns.to_list().index(k))
                except:
                    pass
        nn_ind = []
        for k in n_ind:
            nn_ind.append(temp.columns.to_list()[k])

        if i == "EW1" or i == "EW2":
            outs[i] = temp.reset_index(drop=True).set_index(pd.MultiIndex.from_frame(temp.loc[:, nn_ind])).drop(
                columns=nn_ind).astype(float)
        else:
            data[i] = temp.reset_index(drop=True).set_index(pd.MultiIndex.from_frame(temp.loc[:, nn_ind])).drop(
                columns=nn_ind).astype(float)

    return outs, data_desc, data

def ShapleyExplainability(sv):
    """This function calculates the explainability of the shapley values. It is a simple normalization (mean of absolute values).
    ## Args:
    - sv (pd.DataFrame): Shapley values
    ## Returns:
    - np.array: A numpy array of normalized explainability values"""
    return (np.mean(np.abs(sv.values), axis=0)) #*2 / y_mn*100



def TSFunc(o_var:str, df:pd.DataFrame, func:callable=None, item:str=None, input_vars:dict={}, expl:dict={}, shapley:dict={}, change_expl:dict={}):
    """This function is a wrapper to generalize evaluating expert-defined model. It calculates the Shapley values for the given function,
     depending on the input variables, and adds them to global variables, while returning the output value. If there are multi-indexed data, then it tries to calculate the shapley for each Item.

     ## Args:
     - o_var (str): variable/function name (same az the output variable name)
     - df (pd.DataFrame): input data
     - func (callable): function to be calculated - optional
     - item (str): indicator for multiindexing
     - input_vars (dict[var_name:str, pd.DataFrame]): dictionary of input variables (containing relevant data) -> dependency injection, it IS a global variable required for the analysis.
     - expl (dict[var_name:str, pd.DataFrame]): dictionary of the explainer objects, relevant to SHAP -> dependency injection, it IS a global variable required for the analysis.
     - shapley (dict[var_name:str, pd.DataFrame]): dictionary of the shapley values -> dependency injection, it IS a global variable required for the analysis.
     - change_expl (dict[var_name:str, pd.DataFrame]): dictionary of the explainability values -> dependency injection, it IS a global variable required for the analysis.
     ## Returns:
     - y (pd.DataFrame): The output data

     """
    y = func(df)
    if func is None:
        func = eval(o_var)
    try:
        ex = shap.Explainer(func, df)  ## build an explainer object
        sv = ex(df)  # calculate the shapley values

        ## if the data focuses on a specific item, then we need to handle it differently
        if item is not None:
            try:
                idx = item.split("_")[1] ### if the item has a name with a specifier befor the item type.
            except:
                idx = item ## otherwise continue with the item!

            input_vars[o_var + "_" + idx] = df.columns.tolist()
            expl[o_var + "_" + idx] = ex
            shapley[o_var + "_" + idx] = sv

            change_expl[o_var + "_" + idx] = ShapleyExplainability(sv)  ## scale the shapley values

        else:  ## if the data is not multi-indexed, then we can simply calculate the shapley values
            input_vars[o_var] = df.columns.tolist()
            expl[o_var] = ex
            shapley[o_var] = sv
            change_expl[o_var] = ShapleyExplainability(sv)
    ## otherwise handle buggy/inconsistent data as zero
    except:
        input_vars[o_var] = df.columns.tolist()
        expl[o_var] = 0
        shapley[o_var] = np.zeros((50, 1))
        change_expl[o_var] = np.zeros((len(df.columns.tolist())))
    return y
    # CI[out_var+ "_" + i] = ew_funcs.CI(df)

def compile_input_dataframe():
    """Automatically compiles input dataframes from the input variable dictionary."""
    raise NotImplementedError("This function is not implemented yet!")
