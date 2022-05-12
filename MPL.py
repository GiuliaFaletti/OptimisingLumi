#########################################################
# @Giulia Faletti
# The most probable luminosity model
#########################################################

import numpy as np
import matplotlib.pyplot as plt
import LoadData as ld
from lmfit import Model
import scipy.integrate as integrate

#Font setting
plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Helvetica",
  "font.size": 12
})

#loading fill number
FillNumber16, FillNumber17, FillNumber18 = ld.FillNumber()

#defining the fit function
def fit(x, a, b, c, d):
        return (a*np.exp((-b)*x))+(c*np.exp((-d)*x))


def CuttingAlgorithm(year, text):
    """Function that performs the necessary cut on the current fill

    Args:
        year (int): current year
        text (str): current fill

    Returns:
        T_fit_real: times in second for the cutted data fit
        Y: Luminosity evolution evaluated with the cutted data fit
        a: fitting parameter
        b: fitting parameter
        c: fitting parameter
        d: fitting parameter
    """
    year=str(year)
    f=open('ATLAS/ATLAS_fill_20{}/{}_lumi_ATLAS.txt'.format(year, text),"r")
    lines=f.readlines()
    L_evolx=[]
    times=[]
    for x in lines:
        times.append(int(x.split(' ')[0]))  
        L_evolx.append(float(x.split(' ')[2]))
        
    f.close()
    Times = np.array(times)
    L_evol = np.array(L_evolx)

    #deleting the null values of the luminosity
    zero=np.where(L_evol<100)
    L_zero=np.delete(L_evol, zero)
    T_zero=np.delete(Times, zero)
        
    #check for enough points
    if len(L_zero)<10:
        zero=np.where(L_evol<5)
        L_zero=np.delete(L_evol, zero)
        T_zero=np.delete(Times, zero)

    #defining the derivative 
    dy = np.zeros(L_zero.shape)
    dy[0:-1] = np.diff(L_zero)/np.diff(T_zero)


    #start to slim down the fit interval       
    L_tofit=[]
    T_tofit=[]
    for idx in range(len(L_zero)):
        #cancelling too strong derivative points
        if dy[idx]<0 and dy[idx]>-1.5:
            L_tofit.append(L_zero[idx])
            T_tofit.append(T_zero[idx])
        if dy[idx]>0 or dy[idx]<-1.5:
            continue     
        
    #evaluating the differences between two subsequent points
    diff=np.diff(L_tofit)
        
    #deleting the discrepancies
    thr=np.max(abs(diff))*0.05
    idx_diff= np.where(abs(diff)>thr)[0]+1
        
    #new slim down of data
    L_tofit2=np.delete(L_tofit, idx_diff)
    T_tofit2=np.delete(T_tofit, idx_diff)
        
    #check for enough points
    if len(L_tofit2) < 30:
        L_tofit2=L_tofit
        T_tofit2=T_tofit
        
    L_fit=L_tofit2
    T_fit=T_tofit2     

    L_fit=np.array(L_fit)
    T_fit=np.array(T_fit) 

    #normalization of the fit interval    
    norm_T_fit=[]
    norm_T_fit=np.array(norm_T_fit)
    for element in T_fit:
        z=(element-np.amin(T_fit))/(np.amax(T_fit)-np.amin(T_fit))
        norm_T_fit=np.append(norm_T_fit, z)


    #defining the fit function
    def fit(x, a, b, c, d):
        return (a*np.exp((-b)*x))+(c*np.exp((-d)*x))

    model=Model(fit)      

    #performing fit of last segments of data
    if year=='16':
        model.set_param_hint('b', value=0.2, min=0, max=50)
        model.set_param_hint('d', value=0.2, min=0, max=50)
        model.set_param_hint('a', value=10, min=1, max=8500)
        model.set_param_hint('c', value=10, min=1, max=8500)
        fit_result=model.fit(L_fit, x=norm_T_fit, a=10, b=0.2, c=10, d=0.2)
    elif year=='17':
        model.set_param_hint('b', value=0.2, min=0, max=50)
        model.set_param_hint('d', value=0.2, min=0, max=50)
        model.set_param_hint('a', value=1000, min=1, max=19000)
        model.set_param_hint('c', value=1000, min=1, max=19000)
        fit_result=model.fit(L_fit, x=norm_T_fit, a=1000, b=0.2, c=1000, d=0.2)
    elif year=='18':
        model.set_param_hint('b', value=0.2, min=0, max=50)
        model.set_param_hint('d', value=0.2, min=0, max=50)
        model.set_param_hint('a', value=10, min=1, max=18500)
        model.set_param_hint('c', value=10, min=1, max=18500)
        fit_result=model.fit(L_fit, x=norm_T_fit, a=10, b=0.2, c=10, d=0.2)

    #transforming the times from unix in seconds
    T_fit_real=T_fit-np.amin(T_fit)    
    Y=fit(T_fit_real, fit_result.params['a'].value, (fit_result.params['b'].value/(np.amax(T_fit)-np.amin(T_fit))), fit_result.params['c'].value, fit_result.params['d'].value/(np.amax(T_fit)-np.amin(T_fit)))
    
    return  T_fit_real, Y, fit_result.params['a'].value, (fit_result.params['b'].value/(np.amax(T_fit)-np.amin(T_fit))), fit_result.params['c'].value, fit_result.params['d'].value/(np.amax(T_fit)-np.amin(T_fit))

def PeakLumi(year, text):
    """Function that returns the peak luminosity of the current fill.

    Args:
        year (int): current year
        text (str): current fill

    Returns:
        float: peak luminosity
    """
    T_fit_real, Y, a, b, c, d = CuttingAlgorithm(year, text)  
    peak=Y[0]
    return peak

def SpeedUpMPL(Lpeak, year, fill):
    """Function that evaluates the Most Probable Luminosity.

    Args:
        Lpeak (_type_): peak luminosity of the current fill
        year (int): current year
        fill (int): currebt fill number

    Returns:
        Tmp: most probable times
        Lmp: most probable luminoisties
    """
    
    #defining the mostprobable sampling
    sampling=np.arange(0, 30*3600, 60)
    
    if year==16:
        FillNumber=FillNumber16

    elif year==17:
        FillNumber=FillNumber17
        FillNumber_Prev=FillNumber16
        previous_year=16
    elif year==18:
        FillNumber=FillNumber18
        FillNumber_Prev=FillNumber17
        previous_year=17

    #cleaning file
    with open('MPL/Lmp{}.txt'.format(str(year)), 'w') as f:
        f.write('')
        f.close()


    Lmp=[]
    for samp in sampling:
        Lsamp=[]
        for i1 in range(len(FillNumber_Prev)):
            text = str(int(FillNumber_Prev[i1])) 
            T_fit_real, Y, a1,b1,c1,d1=CuttingAlgorithm(previous_year, text)
            Li=fit(samp, a1, b1, c1, d1)
            L=Li*(Y[0]/Lpeak) #normalisation
            Lsamp.append(L)
    
        for i2 in range(len(FillNumber[:(np.where(FillNumber==(fill))[0][0]+1)])):
            text = str(int(FillNumber[i2])) 
            T_fit_real, Y, a2,b2,c2,d2=CuttingAlgorithm(year, text)
            Li=fit(samp, a2, b2, c2, d2)
            L=Li*(Y[0]/Lpeak) #normalisation
            Lsamp.append(L)
                
        #evaluating the mode
        counts1, bins1=np.histogram(Lsamp)
        max_bin1=np.argmax(counts1)
        mode1=bins1[max_bin1:max_bin1+2].mean()
        
        Lmp.append(mode1)
        with open('MPL/Lmp{}.txt'.format(str(year)), 'a') as f:
            f.write(str(mode1))
            f.write('\n')
            f.close()
    
    Lmp=np.array(Lmp)
    return sampling, Lmp
