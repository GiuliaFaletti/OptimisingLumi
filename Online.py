#########################################################
#      @Giulia Faletti                                  #
# Online optimisation strategy for analysis of 2017     #
#########################################################
from scipy.optimize import least_squares
import scipy.integrate as integrate
import scipy.interpolate
import math
from lmfit import Model
import numpy as np
import matplotlib.pyplot as plt
import LoadData as ld
from MPL import *
#import ConfrontoFitMPL

#font settings
plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Helvetica",
  "font.size": 12
})
#Selecting Current Year
year=17


#loading fill number
FillNumber16, FillNumber17, FillNumber18 = ld.FillNumber()

#load turnaround times and fill times
data_ta16, data_tf16, data_ta17, data_tf17, data_ta18, data_tf18 = ld.loadFill()
data_ta16_sec = data_ta16*3600 
data_tf16_sec = data_tf16*3600  
data_ta17_sec = data_ta17*3600 
data_tf17_sec = data_tf17*3600
data_ta18_sec = data_ta18*3600 
data_tf18_sec = data_tf18*3600


if year==16:
    FillNumber=FillNumber16
    ta=data_ta16_sec
    tf=data_tf16_sec
elif year==17:
    FillNumber=FillNumber17
    FillNumber_Prev=FillNumber16
    previous_year=16
    ta=data_ta17_sec
    tf=data_tf17_sec
elif year==18:
    FillNumber=FillNumber18
    FillNumber_Prev=FillNumber17
    previous_year=17
    ta=data_ta18_sec
    tf=data_tf18_sec

#loading fill evolution fit coefficients  
f=open('Cutting_Fitting/FitCoefficients{}.txt'.format(str(year)),"r")
lines=f.readlines()
a=[]
b=[]
c=[]
d=[]
for x in lines:
    a.append(float(x.split(' ')[1]))
    b.append(float(x.split(' ')[2]))
    c.append(float(x.split(' ')[3]))
    d.append(float(x.split(' ')[4]))  

f.close()
    
a=np.array(a)
b=np.array(b) 
c=np.array(c)
d=np.array(d) 

#defining the fit function
def fit(x, aa, bb, cc, dd):
    return (aa*np.exp((-bb)*x))+(cc*np.exp((-dd)*x))

#loading numerical results - for checking
f=open('NumericalOptimization/res_opt_20{}.txt'.format(str(year)),"r")
lines=f.readlines()
t_opt_num=[]
for x in lines:
    t_opt_num.append(float(x.split(' ')[0]))
    
t_opt_num=np.array(t_opt_num)

#cleaning file for saving the results
with open('Online/FutureFill{}.txt'.format(str(year)), 'w') as f:
    f.write('')
    f.close() 
with open('Online/OptimalFill{}.txt'.format(str(year)), 'w') as f:
    f.write('')
    f.close() 



#defining the mostprobable sampling
sampling=np.arange(0, 30*3600, 60)


#defining the phyisics time
Constraint=np.sum(ta)+np.sum(tf)   

t_future=[]
t_optimal=[]
for i in range(len(FillNumber)):
    fill=FillNumber[i]
    text = str(int(fill)) #number of current fill
    
    #Current Fill Peak Luminosity determination
    L_peak=PeakLumi(year, text)

    #MostProbableLuminosity evaluation
    Tmp, Lmp=SpeedUpMPL(L_peak, year, fill)
    
    print(fill)
    print(sampling)
    print(Tmp)
    print(Lmp)
 
 
 
 
    #check the constraint
    test=np.sum(ta[:i+1])+ sum(t_optimal)
    text1= str(int(FillNumber[i-1]))
    if test>=Constraint:
        print("________________________________________________")
        print("________________________________________________")
        print("| The last fill performed is the fill numered:", text1)
        print("| ", i, "/", len(FillNumber), "fills have been performed.")
        print("________________________________________________")
        print("________________________________________________")
        break
    
    #defining average of the turnaround times
    tau=(np.sum(ta[:i+1]))/(i+1)


