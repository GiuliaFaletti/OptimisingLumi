# How does ONLINEOPTIMISER work?
## @GiuliaFaletti
The OnlineOptimiser allow the user to find the optimal values of fill times for the LHC.
The folder contains:
* **ATLAS**: Folder with Massi files data (istantaneous luminosity and integrated ones) and graphs of luminosity evolutions;
* **Cutting_Fitting**: Folder that stores the results of the Cutting_Fitting.py script;
* **MPL**: Folder that stores the most probable luminosity model of each year;
* **NumericalOptimization**: Folder that stores the results of the numerical optimiser;
* **Online**: Folder that stores the results of the online optimisations (Future fill times and optimal fill times);
* **Cutting_Fitting.py**: Script that performs the necessary cuts and fits for all selected fills;
* **LoadData.py**: Script that loads the needed data from FillData.xlsx;
* **MPL.py**: Most Probable luminosity model;
* **NumericalOptimisation.py**: Numerical optimisation of the Run 2 control room operations;
* **Online.py**: Script that performs the online optimisation;
* **FillData.xlsx**: Stores the preselected fills number, times and turnaround times for the studied years (2016-2017-2018).

## More on MPL.py

1. ***CuttingAlgorithm***:
2. ***PeakLumi***:
3. ***SpeedUpMPL***:

## More on Online.py


