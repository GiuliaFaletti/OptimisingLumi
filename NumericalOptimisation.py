import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.integrate import quad
import LoadData as ld

plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Helvetica",
  "font.size": 12
})

#selecting current year
year=18

#loading fill number
FillNumber16, FillNumber17, FillNumber18 = ld.FillNumber()

#load turnaround times and fill times - cheking
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


#model parameters and initial guesses
a=np.array(a)
b=np.array(b)
c=np.array(c)
d=np.array(d)


#Objective Function
def fun(t1):
    result=np.empty(len(x0))
    for i in range(len(x0)):
        lam=lambda x1: a[i]*np.exp(-(b[i]*x1))+c[i]*np.exp(-d[i]*x1)
        result[i]=-quad(lam, 0, t1[i])[0]
        
    result = np.sum(result)
    return result

#constraint
def cons(t1):
    res = np.sum(t1) - (tot)
    return res

#jacobian of the objective function
def jacb(t1):
    der=-a*np.exp(-(b*t1))-c*np.exp(-d*t1)
    #result=np.sum(der)
    return der
        
    
#Initial guesses    
x0=tf

#constraint determination
tot=sum(x0)

#bounds
list=[[1800, 28*3600]]
for li in range(1, len(a)):
    list=list+[[1800, 28*3600]]
        
bnd=list

#optimization
res = minimize(fun, x0, options={'disp': True, 'maxiter':10000}, constraints={'type':'eq', 'fun': cons, 'jac': lambda x: np.ones(len(x0))}, jac=jacb, method='SLSQP', bounds=bnd) #      

#saving optimized times
with open('NumericalOptimization/res_opt_20{}.txt'.format(str(year)), 'w') as f:
        f.write('')
        f.close()
for el in res.x:
    with open('NumericalOptimization/res_opt_20{}.txt'.format(str(year)), 'a') as f:
        f.write(str(el))
        f.write('\n')


