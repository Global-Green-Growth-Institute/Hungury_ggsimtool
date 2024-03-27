![alt text](http://greengrowthindex.gggi.org/wp-content/uploads/2019/09/LOGO_GGGI_GREEN_350x131px_002trans_Prancheta-1.png)

# Hungury Simulation Dashboard
Hungury Simulation Dashboard is a web application for policy simulation. It is deployed at https://hungary-simtool.herokuapp.com/

## Purpose
The goal of this application is to display the simulation results. The app is divided into two components. The first is the simulation tool which allows to interact with models and simulate policies and the second is the evidence librabry which includes all the models, data and codes used in the analysis. 

## Installation
-------------------
```
$ git clone https://github.com/Global-Green-Growth-Institute/Hungury_ggsimtool.git

$ python index.py
```

## Deployment
-------------------
The app can be deployed on Heroku via:

```
$ git push heroku Hungury_ggsimtool
```

Go to https://devcenter.heroku.com/articles/git for more details


## Project Structure 

    ├── data           
    │   
    │   └── System dynamic Model <- System dynamic Model data and Analysis
    │   └── Network Analysis     <- Network Analysis
    │   └── Shapnet              <- Shapnet Analysis
    |   └── Correlation Alayisis  <- Correlation Anayisis 
    ├── assets                    <- css and background
    |
    ├── ggmodel_dev               <- Graphmodel computation package
    |
    ├── outputs                   <- Ressources downloadables in the interface
    |
    ├── pages                     <- Source code of individual pages

# Roadmap

Code: 
- Fetch simulation data and model from external database
- Improve modularity by using a sub repo for ggmodel_dev.
- Improve simulation page to add new models more easily

Features:
- Enhance data storage efficiency in the cloud database
- Improve downloadable pdf report
- Add data explorer for simulation models

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# Contact
----------------
Program Manager: A. Lilibeth - lilibeth.acosta@gggi.org<br>
Programmer: I. Nzimenyera - innocent.nzimenyera@gggi.org<br>
Programmer: R. Mihigo - munezero.ribeus@gggi.org<br>
Programmer: A. Ipkovich - ipkovichadam@gmail.com<br>
Data Analsyt: R. Sabado - ruben.jr@gggi.org<br>
Analsyt: J. Julia - julia.joveneau@gggi.org


