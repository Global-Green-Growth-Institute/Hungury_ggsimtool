"""This module is a singleton containing all computations. There are supporting methods in vizu.py and wrappers.py
The function of this module is to export figures so that it can be used in the website.
NOTE: This is a very long script, but it is not complicated. It is just a lot of data wrangling and calculations.
THERE ARE REDUNDANT PARTS IN THE CODE, BUT IT IS EASIER TO HANDLE THIS WAY!
NOTE: THIS IS NOT INTEGRATED WITH GRAPHMODELS YET!
NOTE: SHAP-BASED ANALYSIS CANNOT BE A RUNTIME FEATURE, BECAUSE IT IS TOO SLOW!
"""

__author__ = "Ádám Ipkovich"
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import warnings
import os
import pickle
from functools import partial

from utils import *

warnings.filterwarnings("ignore")

height_rice = 0.2  # meter height of rice
ha_to_m2 = 1e4
mm_to_m = 1e-2
mmyear_to_m3year = 1e-2  # from mm/year to m3/year as 1mm = 10m3/ha \n",

#%% Read Data

address = os.path.join(os.getcwd(), "shap_backend", "data_new5_n.xlsx")
xls = pd.ExcelFile(address) # read excel file

outs, data_desc, data = read_EW_data(address)
# %% Initialize global variables !!!
val_data = data
input_vars = {}
expl = {}
shapley = {}
change_expl = {}
##So that we can use the global variables in the functions without manually adding them to each one.
ShapNet = partial(TSFunc, input_vars = input_vars, expl = expl, shapley = shapley, change_expl = change_expl )

#%% EW1 model
########################################

# generally speaking there are 2 parts of evaluation:
# define the model
# then use the evaluation function to calculate the shapley values
# CODE SAVES EVERYTHING IN A GLOBAL VARIABLE TO EXPORT AND USE IN THE WEBSITE IF NEED BE!!!!

#%% CI

    
def CI(X): #ICA, AIR
    params =  data["ICA"].reset_index(drop=True).iloc[idx].values[0] 
    return params/X.loc[:, ["AIR"]].reset_index(drop = True)

out_var = "CI"  
df = data["AIR"]

data[out_var] = pd.DataFrame()
items = data["ICA"].unstack(1).columns.tolist()
for idx, i in enumerate(items):
    i = i[1]
    dy = ShapNet(out_var, df, func = CI, item = i)
    dy.columns = [out_var + "_" + i]
    if data[out_var].empty:
        data[out_var] = dy
    else:
        data[out_var] = pd.concat([data[out_var].reset_index(drop=True), dy.reset_index(drop=True)], axis = 1)     

#%% ETc

def ETc(X): # Kc, CI, ETo
    params = np.repeat(data["Kc"].values, X.shape[0], axis=1).transpose()
    y =  np.sum(params*X.iloc[:, 1::] * np.repeat(X.loc[:, ["ETo"]].values, 9, axis = 1), axis=1)
    return y


out_var = "ETc" 
df = pd.concat([data["ETo"].reset_index(drop=True),  data["CI"].reset_index(drop=True)], axis = 1)
params = np.repeat(data["Kc"].values, data["ETo"].shape[0], axis=1).transpose()
data[out_var] = ShapNet(out_var, df, func = ETc)

data[out_var].name = out_var
#%% ICU
def ICU(X):
    return np.abs(X.loc[:, "ETc"] - X.loc[:, "ETa"])

out_var = "ICU"
df = pd.concat([data["ETc"],  data["ETa"].reset_index(drop=True)], axis = 1)
data[out_var] = ShapNet(out_var, df, func = ICU)
data[out_var].name = out_var
#%% AIRi - "IRRTECHi","AIR"

def AIRi(X):
    return X.iloc[:, 1] * X.loc[:, "AIR"]

out_var = "AIRi"
df = data["AIR"]
dum = data["IRRTECHi"].unstack(level=2)
items = ["IRRTECHi_" + i[1] for i in dum.columns.tolist()]
dum.columns = items
expl[out_var] = {}
shapley[out_var] = {}

data[out_var] = pd.DataFrame()
input_vars[out_var] = []
for i in items:
    
    dx = pd.concat((df, dum.loc[:, i]), axis = 1).reset_index(drop=True)

    input_vars[out_var + "_" + i.split("_")[1]] = dx.columns.to_list()
    dy = ShapNet(out_var, dx, func = AIRi, item = i)
    dy.name = out_var + "_" + i.split("_")[1]

    if data[out_var].empty:
        data[out_var] = dy.to_frame()
    else:
        data[out_var] = pd.concat([data[out_var], dy], axis = 1)    


#%% IWRi

def IWRi(X): # ICU, AIRi - changes
    return 1e-9 * ha_to_m2 * mmyear_to_m3year *  X.loc[:, "ICU"] * X.iloc[:, 1]

out_var = "IWRi"
df = data["ICU"].to_frame()

expl[out_var] = {}
shapley[out_var] = {}
input_vars[out_var] = []
data[out_var] = pd.DataFrame()
for i in data["AIRi"].columns:
    dx = pd.concat([df.reset_index(drop=True), data["AIRi"].loc[:, i]], axis = 1).reset_index(drop=True)
    input_vars[out_var + "_" + i.split("_")[1]] = dx.columns.to_list()
    dy = ShapNet(out_var, dx, func = IWRi, item = i)
    dy.name = out_var + "_" + i.split("_")[1]
    if data[out_var].empty:
        data[out_var] = dy.to_frame()
    else:
        data[out_var] = pd.concat([data[out_var], dy], axis = 1) 
        
#%% IWW

def IWW(X): # IWRi! Arice, IRRTECHEFFi
    params =  np.repeat(data["IRRTECHEFFi"].values, X.shape[0], axis=1).transpose()# np.multiply( ,  np.repeat(data["CE"].values, X.shape[0], axis=1).transpose())
    return np.sum(X.iloc[:, 0:3]/params, axis = 1) + X.loc[:, "Arice"]* height_rice

out_var = "IWW"
df = pd.concat([data["IWRi"], data["Arice"].reset_index(drop=True)], axis = 1)

data[out_var] = ShapNet(out_var, df, func = IWW)
data[out_var].name = out_var
#%% AWU
def AWU(X):
    return X

out_var = "AWU"
df = data["IWW"].to_frame()
dd = ShapNet(out_var, df, func = AWU)

dd.columns = [out_var]
data[out_var] = dd
#%% MWU

def MWU(X):
    return np.exp(-0.9522) *  X.loc[:, "WP"]**(- 0.3174)  * X.loc[:, "GDPC"]**0.5918827 * X.loc[:, "Pop"]**(0.9859812) * 1e-9


out_var = "MWU"
df = pd.DataFrame()
df = data["WP"]
df = pd.concat([df, data["GDPC"], data["Pop"]], axis = 1)

data[out_var] = ShapNet(out_var, df, func = MWU)
data[out_var].name = out_var
#%%TWW

def TWW(X):
    return np.sum(X, axis=1)

out_var = "TWW"
df = pd.DataFrame()
df = data["MWU"].to_frame().reset_index(drop = True)
df = pd.concat([df, data["AWU"].reset_index(drop = True), data["IWU"].reset_index(drop = True)], axis = 1)
data[out_var] = ShapNet(out_var, df, func = TWW)
data[out_var].name= out_var

#%% PAIR

def PAIR(X): #ICA is a parameter - only input CL
    params = data["ICA"].reset_index(drop=True)
    return np.sum(params)[0]/X.reset_index(drop=True)
out_var = "PAIR"
df = data["CL"]
data[out_var] = ShapNet(out_var, df, func = PAIR)
data[out_var].columns = [out_var]
#%% Cr

def Cr(X): # only input PAIR
    return 1/(1+(X/(1-X)*0.563))

out_var = "Cr"
df = data["PAIR"]
data[out_var] = ShapNet(out_var, df, func = Cr)
data[out_var].columns = [out_var]
#%% EW1
def EW1(X): # inputs: TWW, AGVA, IGVA, SGVA, Cr
    return  (X.loc[:, "AGVA"] * (1 - X.loc[:, "Cr"]) + X.loc[:, "IGVA"] + X.loc[:, "SGVA"]) / (X.loc[:, "TWW"]* 1e9)

out_var = "EW1"
df = pd.concat([data["TWW"].reset_index(drop=True), data["AGVA"].reset_index(drop=True), data["IGVA"].reset_index(drop=True), data["SGVA"].reset_index(drop=True), data["Cr"].reset_index(drop=True)], axis = 1)
data[out_var] = ShapNet(out_var, df, func = EW1)
data[out_var].columns = [out_var]


#%% EW2
################################################
#%%TRF - two constants...
def TRF(X): # IRWR, ERWR
    return X.loc[:, "IRWR"] + X.loc[:,  "ERWR"]

out_var = "TRF"
df = pd.concat([data["IRWR"].reset_index(drop=True), data["ERWR"].reset_index(drop=True)], axis = 1)
data[out_var] = ShapNet(out_var, df, func = TRF)
data[out_var].name = out_var

#%% TNCW

def TNCW(X): # DW, TW
    return X.loc[:, "DW"] + X.loc[:, "TW"]

out_var = "TNCW"
df = pd.concat([data["DW"].reset_index(drop=True), data["TW"].reset_index(drop=True)], axis = 1)
data[out_var] = ShapNet(out_var, df, func = TNCW)
data[out_var].name = out_var

#%% TFA

def TFA(X): # TRF, TNCW
    return X.loc[:, "TRF"] + X.loc[:, "TNCW"]

out_var = "TFA"
df = pd.concat([data["TRF"].reset_index(drop=True), data["TNCW"].reset_index(drop=True)], axis = 1)
data[out_var] = ShapNet(out_var, df, func = TFA)
data[out_var].name = out_var


#%% EW2

def EW2(X): # TWW, TFA, EFR
    params = data["EFR"].iloc[0][0]
    return X.loc[:, "TWW"] / (X.loc[:, "TFA"] -params)*1e2 

out_var = "EW2"
df = pd.concat([data["TWW"].reset_index(drop=True), data["TFA"]], axis = 1)
data[out_var] = ShapNet(out_var, df, func = EW2)
data[out_var].columns = [out_var]



#%% Indirect Shapley - ONE FUNCTION CONTAINS ALL COMPUTATIONS!

def EW1_wrapper(X):
    
    n_data = X.reset_index(drop=True)
    out_var = "CI"  
    df = n_data.loc[:, ["AIR"]].reset_index(drop=True)
    
    items = data["ICA"].unstack(1).columns.tolist()
    for idx, i in enumerate(items):
        dy = eval(out_var + "(df)")
        dy.columns =[ out_var + "_" + i[1]]
        n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    # ETc
    out_var = "ETc" 
    df = n_data.loc[:, ["ETo",
                        'CI_fruit',
                        'CI_maize',
                        'CI_pastures',
                        'CI_potatoes',
                        'CI_pulses',
                        'CI_rapeseed',
                        'CI_sugar beet',
                        'CI_sunflower',
                        'CI_vegetables']]
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    
    out_var = "ICU"
    df = n_data.loc[:, ["ETc", "ETa"]]   
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "AIRi"
    df = n_data.loc[:, ["AIR"]].reset_index(drop=True)
    items = ["IRRTECHi_" + i for i in ["Drip", "Sprinkler", "Surface"]]

    for i in items:
        dx = pd.concat((df, n_data.loc[:, [i]].reset_index(drop=True)), axis = 1)
        dy = eval(out_var + "(dx)")
        dy.name = out_var + "_" + i.split("_")[1]
        n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "IWRi"
    df = n_data.loc[:, ["ICU"]]
    for i in data["AIRi"].columns:
        dx = pd.concat([df.reset_index(drop=True), n_data.loc[:, [i]]], axis = 1).reset_index(drop=True)
        dy = eval(out_var + "(dx)")
        dy.name = out_var + "_" + i.split("_")[1]
        n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    
    out_var = "IWW"
    df = n_data.loc[:, ["IWRi_Drip", "IWRi_Sprinkler", "IWRi_Surface", "Arice"]] 
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "AWU"
    df = n_data.loc[:, ["IWW"]]
    dy = eval(out_var + "(df)")
    dy.columns = [out_var]
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "MWU"
    df = n_data.loc[:, ["WP", "GDPC", "Pop"]]
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)

    out_var = "TWW"
    df = n_data.loc[:, ["MWU", "AWU", "IWU"]].reset_index(drop = True)
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)    

    out_var = "PAIR"
    df = n_data.loc[:, ["CL"]]
    dy = eval(out_var + "(df)")
    dy.columns = [out_var]
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)  
    
    out_var = "Cr"
    df = df = n_data.loc[:, ["PAIR"]]
    dy = eval(out_var + "(df)")
    dy.columns = [out_var]
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "EW1"
    df = n_data.loc[:, ["TWW", "AGVA", "IGVA", "SGVA", "Cr"]] 
    dy = eval(out_var + "(df)")
    dy.name = out_var
    
    return dy

#%%

ew1_vars = ["AIR", "ETo", "ETa", "IRRTECHi", "Arice", "WP", "GDPC", "Pop", "CL", "IWU", "AGVA", "IGVA", "SGVA"]
ew1_data = pd.DataFrame()
for i in ew1_vars:
    
    n_v = []
    if i == "IRRTECHi":
       n_v = val_data[i].unstack(level=2)
       n_v.columns = ["IRRTECHi_Drip", "IRRTECHi_Sprinkler", "IRRTECHi_Surface"]
    else:
       n_v = val_data[i]
    
    if ew1_data.empty:
        ew1_data = n_v
    else:
        ew1_data = pd.concat((ew1_data, n_v), axis = 1)

ew1_data = pd.DataFrame(ew1_data)

ex_ew1 = shap.Explainer(EW1_wrapper, ew1_data.reset_index(drop=True))
sv_ew1 = ex_ew1(ew1_data.reset_index(drop=True))


### Visualie indirect shapley (input varaible contributions to the output WITHOUT intermediate variables)
plt.figure(2)
shap.plots.waterfall(sv_ew1[17], max_display=14)
shap.plots.bar(sv_ew1)
shap.plots.beeswarm(sv_ew1)


#%% EW2 wrapper

def EW2_wrapper(X):
    n_data = X.reset_index(drop=True)
    out_var = "CI"  
    df = n_data.loc[:, ["AIR"]].reset_index(drop=True)
    
    items = data["ICA"].unstack(1).columns.tolist()
    for idx, i in enumerate(items):
        dy = eval(out_var + "(df)")
        dy.columns = [out_var + "_" + i[1]]
        n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    # ETc
    out_var = "ETc" 
    df = n_data.loc[:, ["ETo",
                        'CI_fruit',
                        'CI_maize',
                        'CI_pastures',
                        'CI_potatoes',
                        'CI_pulses',
                        'CI_rapeseed',
                        'CI_sugar beet',
                        'CI_sunflower',
                        'CI_vegetables']]
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    
    out_var = "ICU"
    df = n_data.loc[:, ["ETc", "ETa"]]   
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "AIRi"
    df = n_data.loc[:, ["AIR"]].reset_index(drop=True)
    items = ["IRRTECHi_" + i for i in ["Drip", "Sprinkler", "Surface"]]

    for i in items:
        dx = pd.concat((df, n_data.loc[:, [i]].reset_index(drop=True)), axis = 1)
        dy = eval(out_var + "(dx)")
        dy.name = out_var + "_" + i.split("_")[1]
        n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "IWRi"
    df = n_data.loc[:, ["ICU"]]
    for i in data["AIRi"].columns:
        dx = pd.concat([df.reset_index(drop=True), n_data.loc[:, [i]]], axis = 1).reset_index(drop=True)
        dy = eval(out_var + "(dx)")
        dy.name = out_var + "_" + i.split("_")[1]
        n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    
    out_var = "IWW"
    df = n_data.loc[:, ["IWRi_Drip", "IWRi_Sprinkler", "IWRi_Surface", "Arice"]] 
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "AWU"
    df = n_data.loc[:, ["IWW"]]
    dy = eval(out_var + "(df)")
    dy.columns = [out_var]
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "AWU"
    df = n_data.loc[:, ["IWW"]]
    dy = eval(out_var + "(df)")
    dy.columns = [out_var]
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "MWU"
    df = n_data.loc[:, ["WP", "GDPC", "Pop"]]
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)

    out_var = "TWW"
    df = n_data.loc[:, ["MWU", "AWU", "IWU"]].reset_index(drop = True)
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)    
    
    out_var = "TRF"
    df = n_data.loc[:, ["IRWR", "ERWR"]]
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)    
    
    out_var = "TNCW"
    df = n_data.loc[:, ["DW", "TW"]] 
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)   
    
    out_var = "TFA"
    df = n_data.loc[:, ["TRF", "TNCW"]]
    dy = eval(out_var + "(df)")
    dy.name = out_var
    n_data = pd.concat((n_data, dy.reset_index(drop=True)), axis = 1)
    
    out_var = "EW2"
    df = n_data.loc[:, ["TWW", "TFA"]]
    dy = eval(out_var + "(df)")
    dy.name = out_var
    return dy

#%% Evaluation of models

ew2_vars = ["AIR", "ETo", "ETa", "IRRTECHi", "Arice", "IWU", "WP", "GDPC", "Pop", "IRWR", "ERWR", "DW", "TW"]
ew2_data = pd.DataFrame()
for i in ew2_vars:
    
    n_v = []
    if i == "IRRTECHi":
       n_v = val_data[i].unstack(level=2)
       n_v.columns = ["IRRTECHi_Drip", "IRRTECHi_Sprinkler", "IRRTECHi_Surface"]
    else:
       n_v = val_data[i]
    
    if ew2_data.empty:
        ew2_data = n_v
    else:
        ew2_data = pd.concat((ew2_data, n_v), axis = 1)

ew2_data = pd.DataFrame(ew2_data)

ex_ew2 = shap.Explainer(EW2_wrapper, ew2_data.reset_index(drop=True))
sv_ew2 = ex_ew2(ew2_data.reset_index(drop=True))

plt.figure(3)
shap.plots.waterfall(sv_ew2[17], max_display=14)
shap.plots.bar(sv_ew2)
shap.plots.beeswarm(sv_ew2)

#######################################################
#%%MACHINE LEARNING SECTION TO CHECK THE RESULTS

#%%EW1 ML
reg = LinearRegression().fit(ew1_data.reset_index(drop=True).iloc[0:10, :], outs["EW1"].iloc[0:10])
lr_ew1 =reg.predict(ew1_data.reset_index(drop=True))
ex = shap.Explainer(reg.predict, ew1_data.reset_index(drop=True))
shapley["EW1_LR"] = ex(ew1_data.reset_index(drop=True))

from sklearn.neighbors import KNeighborsRegressor
neigh = KNeighborsRegressor(n_neighbors=3)
neigh.fit(ew1_data.iloc[:, :], outs["EW1"].iloc[:])
knn_ew1 = neigh.predict(ew1_data.reset_index(drop=True))

print(r2_score(outs["EW1"], lr_ew1))

#%%EW2 LR
reg = LinearRegression().fit(ew2_data.reset_index(drop=True).iloc[0:10, :], outs["EW2"].iloc[0:10, :])
lr_ew2 =reg.predict(ew2_data.reset_index(drop=True))
ex = shap.Explainer(reg, ew2_data.reset_index(drop=True))
shapley["EW2_LR"] = ex(ew2_data.reset_index(drop=True))

#%% knn ew2

neigh = KNeighborsRegressor(n_neighbors=3)
neigh.fit(ew2_data.iloc[:, :], outs["EW2"].iloc[:])
knn_ew2 = neigh.predict(ew2_data.reset_index(drop=True))

#%% MWU parameter optimization -- THIS IS AN EXAMPLE TO IMPROVE THE MODEL!
from scipy.optimize import minimize
from scipy.optimize import basinhopping

def param_opt_ew1(theta, X, ind):
    mwu = np.exp(theta[0]) *  X["WP"].reset_index(drop=True).squeeze()[ind[0]:ind[1]]**(theta[1]) * X["GDPC"].reset_index(drop=True).squeeze()[ind[0]:ind[1]]**theta[2]*X["Pop"].reset_index(drop=True).squeeze()[ind[0]:ind[1]] **(theta[3]) * 1e-9
    #mwu = np.exp(theta[0] + theta[1] * np.log(X["WP"].reset_index(drop=True)).squeeze()[ind[0]:ind[1]] + theta[2] * np.log(X["GDPC"].reset_index(drop=True)).squeeze()[ind[0]:ind[1]] + theta[3] * np.log(X["Pop"].reset_index(drop=True)).squeeze()[ind[0]:ind[1]] ) * 1e-9
    tww = mwu.reset_index(drop = True).squeeze()  + X["AWU"].squeeze().reset_index(drop = True)[ind[0]:ind[1]].reset_index(drop = True)  + X["IWU"].reset_index(drop = True).squeeze()[ind[0]:ind[1]].reset_index(drop = True)
    cr = 1/(1+(X["PAIR"].reset_index(drop = True)[ind[0]:ind[1]].reset_index(drop = True) /(1-X["PAIR"].reset_index(drop = True))[ind[0]:ind[1]].reset_index(drop = True) *0.562))
    return (X["AGVA"].reset_index(drop = True).squeeze()[ind[0]:ind[1]].reset_index(drop = True)  * (1 - cr.squeeze().reset_index(drop = True)) 
            + X["IGVA"].reset_index(drop = True).squeeze()[ind[0]:ind[1]].reset_index(drop = True) 
            + X["SGVA"].reset_index(drop = True).squeeze()[ind[0]:ind[1]] .reset_index(drop = True))  /(tww.reset_index(drop = True) * 1e9), tww.reset_index(drop = True) 

def param_opt_ew2(TWW, ind):
    return TWW / (data["TFA"][ind[0]:ind[1]].reset_index(drop = True)  -data["EFR"].iloc[0][0])*1e2 


def param_opt_func(theta, *args):
    X, y_ew1, y_ew2, ind = args
    y_hat_ew1, tww = param_opt_ew1(theta, X, ind)
    y_hat_ew2 = param_opt_ew2(tww.squeeze(), ind)
    print(np.mean((y_ew1.values-y_hat_ew1.values)**2) + np.mean((y_ew2.values-y_hat_ew2.values)**2)*20)
    return np.mean((y_ew1.values-y_hat_ew1.values)**2) + np.mean((y_ew2.values-y_hat_ew2.values)**2)*20
    

#minimizer_kwargs = {"method":"L-BFGS-B", "args"  : (data, outs["EW1"], outs["EW2"], (0, 20)), "bounds" : ( (-1000, 0), (-1000, 0), (0, 1000), (0, 1000)) } #"bounds" : ((-10, 10), (-10, 10), (-10, 10), (-10, 10))
res =  minimize(param_opt_func, [-0.9522 ,- 0.3174, 0.5918827, 0.9859812, 0.563], args= (data, outs["EW1"], outs["EW2"], (0, 20)), method='L-BFGS-B', bounds=((-0.953, -0.95) ,(- 0.317, - 0.31), (0.58,0.6) , (0.92, 1), (0.55, 0.57))) #"L-BFGS-B"
opt_ew1, tww= param_opt_ew1(res.x, data, (0, 20))
#((-0.999, -0.8) ,(- 0.5, -0.1), (0.4, 0.8) , (0.8, 0.999), (0.4, 0.6))
#
opt_ew2 = param_opt_ew2(tww, (0, 20)) 

#%% VIZUALIZATION OF TIME SERIES AND PREDICTED DATA
import matplotlib as mpl

#plt.rcParams['text.usetex'] = True
fig, axs = plt.subplots(2, 2, figsize=(15, 15))

plt.subplot(2, 1, 1)
plt.plot(np.arange(2000,2020), outs["EW1"].values, color= "red", linewidth='4', label = "Observed")
plt.plot(np.arange(2000,2020), data["EW1"].values, color="blue", linestyle = "--", linewidth='4', label = "GGSim")
plt.plot(np.arange(2000,2020), opt_ew1.values, color="orange", linestyle = ":", linewidth='4', label = "Parameter Optimized GGSim model")
#plt.plot(np.arange(2000,2020), np.concatenate((opt_ew11.values, opt_ew12.values)), color="grey", linestyle = ":", linewidth='4') #, opt_ew13.values
plt.plot(np.arange(2000,2020), lr_ew1, color="green", linestyle = "-.", linewidth='4', label="Linear regression")
plt.plot(np.arange(2000,2020), knn_ew1, color="black", linestyle = "-.", linewidth='4', label="k-th nearest neighbors")
#plt.plot(np.arange(2000,2020), ch_ew1, color="black", linestyle = "-.", linewidth='4')
plt.ylabel(r"SDG 6.4.1: Water use efficency [\$/($m^3$/year)]")
plt.xticks(ticks = np.arange(2000,2020,1))
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(np.arange(2000,2020), outs["EW2"].values, color= "red",  label = "Observed", linewidth='4')
plt.plot(np.arange(2000,2020), data["EW2"].values, color ="blue",linestyle = "--", label = "GGSim", linewidth='4')
plt.plot(np.arange(2000,2020), opt_ew2.values, color="orange", linestyle = ":", label = "Parameter Optimized GGSim model", linewidth='4', )
plt.plot(np.arange(2000,2020), lr_ew2, color="green", linestyle = "-.", label="Linear regression", linewidth='4')
plt.plot(np.arange(2000,2020), knn_ew2, color="black", linestyle = "-.", linewidth='4', label="k-th nearest neighbors")

#plt.plot(np.arange(2000,2020), dl_res2, color="black", linestyle = "-.", linewidth='4', label="Neural Network")

#plt.plot(np.arange(2000,2020), ch_ew2, color="black", linestyle = "-.", linewidth='4', label = "Indirect predicted")
plt.xlabel("Year")
plt.ylabel(r"SDG 6.4.2: Share of Freshwater Withdrawal to Freshwater Availability [%]")
plt.xticks(ticks = np.arange(2000,2020,1))
plt.legend()



#%%Retrain model lw2 modell

reg = LinearRegression().fit(ew2_data.reset_index(drop=True).iloc[3:13, :], outs["EW2"].iloc[3:13, :])
lr_ew22 =reg.predict(ew2_data.iloc[3::, :].reset_index(drop=True))

#plt.rcParams['text.usetex'] = True

fig, axs = plt.subplots(1, 1, figsize=(15, 7))
plt.plot(np.arange(2003,2020), outs["EW2"].values[3::], color= "red",  label = "Observed", linewidth='4')
plt.plot(np.arange(2003,2020), lr_ew2[3::], color="green", linestyle = "-.", label="Linear regression", linewidth='4')
plt.plot(np.arange(2003,2020), lr_ew22, color="c", linestyle = "-.", label="Linear regression retrained", linewidth='4')
plt.xlabel("Year")
plt.ylabel(r"SDG 6.4.2: Share of Freshwater Withdrawal to Freshwater Availability [%]")
plt.legend()

#%% VIZUALIZE SHAPLEY NETWORK
from vizu import *
sc_change_expl = GetShapWeight(change_expl)

centralities = {}

node_names = list(np.unique(ew1_data.columns.tolist() + ew2_data.columns.tolist() + list(change_expl.keys())))
G = BuildGraph(change_expl, node_names, input_vars, shapley, row_ind = None) # CHeck vizualization.py
g,ll = ToiGraph(G) #-.-

w = [np.abs(i[0]) + 0.0000001 for i in g.es["edge_width"]]
centralities["betweenness"] = {"mean": g.betweenness(directed=True, weights = w)}
centralities["closeness"]  ={"mean": g.closeness(vertices=None, mode = 'all', weights = w)}
centralities["degree"] = {"mean" :  g.degree(mode="ALL")}


#marker_scaler = g.betweenness(directed=True, weights = [i[0] + 0.001 for i in g.es["weight"]])
fig_ind = Vizualize_iGraph_Plotly(g, ll,  marker_scaler = [])
fig_dir = os.path.join(os.getcwd(), "shap_backend", "figs", "EW")
fig_data = fig_ind.to_dict()
with open(os.path.join(fig_dir, "shap_net_mean_None.pkl"), "wb") as out_file:
    pickle.dump(fig_data, out_file)

fig_ind = Vizualize_iGraph_Plotly(g, ll, marker_scaler = centralities["betweenness"]["mean"], show_weight = False, show_node_size = True)
fig_dir = os.path.join(os.getcwd(), "shap_backend", "figs", "EW")
fig_data = fig_ind.to_dict()
with open(os.path.join(fig_dir, "shap_net_mean_betweenness.pkl"), "wb") as out_file:
    pickle.dump(fig_data, out_file)

fig_ind = Vizualize_iGraph_Plotly(g, ll, marker_scaler = centralities["closeness"]["mean"], show_weight = False, show_node_size = True)
fig_dir = os.path.join(os.getcwd(), "shap_backend", "figs", "EW")
fig_data = fig_ind.to_dict()
with open(os.path.join(fig_dir, "shap_net_mean_closeness.pkl"), "wb") as out_file:
    pickle.dump(fig_data, out_file)

fig_ind = Vizualize_iGraph_Plotly(g, ll,  marker_scaler = centralities["degree"]["mean"], show_weight = False, show_node_size = True)
fig_dir = os.path.join(os.getcwd(), "shap_backend", "figs", "EW")
fig_data = fig_ind.to_dict()
with open(os.path.join(fig_dir, "shap_net_mean_degree.pkl"), "wb") as out_file:
    pickle.dump(fig_data, out_file)

for i in range(0, 20):
    G = BuildGraph(change_expl, node_names, input_vars, shapley, row_ind =i)
    g,ll = ToiGraph(G)
    w = [np.abs(j[0]) + 0.0000001 for j in g.es["edge_width"]]
    centralities["betweenness"][str(i)] = g.betweenness(directed=True, weights=w)
    centralities["closeness"][str(i)] = g.closeness(mode='all', weights=w)
    centralities["degree"][str(i)] =  g.degree(mode="ALL")

    fig_ind = Vizualize_iGraph_Plotly(g, ll,  marker_scaler = [])
    fig_data = fig_ind.to_dict()
    with open(os.path.join(fig_dir, f"shap_net_{i}_None.pkl"), "wb") as out_file:
       pickle.dump(fig_data, out_file)

    fig_ind = Vizualize_iGraph_Plotly(g, ll,  marker_scaler = centralities["betweenness"][str(i)], show_weight = False, show_node_size = True)
    fig_data = fig_ind.to_dict()
    with open(os.path.join(fig_dir, f"shap_net_{i}_betweenness.pkl"), "wb") as out_file:
       pickle.dump(fig_data, out_file)


    fig_ind = Vizualize_iGraph_Plotly(g, ll,  marker_scaler = centralities["closeness"][str(i)], show_weight = False, show_node_size = True)
    fig_data = fig_ind.to_dict()
    with open(os.path.join(fig_dir, f"shap_net_{i}_closeness.pkl"), "wb") as out_file:
       pickle.dump(fig_data, out_file)


    fig_ind = Vizualize_iGraph_Plotly(g, ll,  marker_scaler = centralities["degree"][str(i)], show_weight = False, show_node_size = True)
    fig_data = fig_ind.to_dict()
    with open(os.path.join(fig_dir, f"shap_net_{i}_degree.pkl"), "wb") as out_file:
       pickle.dump(fig_data, out_file)


