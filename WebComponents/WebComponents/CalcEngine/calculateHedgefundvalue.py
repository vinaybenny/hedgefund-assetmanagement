import numpy
from numpy import matrix
from scipy.stats import norm

import SimulationParams
from HfAlpha_LeverageIterator import HfAlpha_LeverageIterator


# Added for testing, remove later
import pylab as py
import matplotlib.pyplot as plt # Added for testing, remove later
from numpy.fft import fft
import mpl_toolkits.mplot3d.axes3d as p3

def calcHedgefundvalue(parameter_vals):

    # Define the range of values of alpha_hf and leverage_hf for loop iteration
    #-----The values should come from the request xml file-----
    initWealth = parameter_vals.initWealth
    alpha_hf_min = parameter_vals.alpha_hf_min

    alpha_hf_max = 0.08
    leverage_hf_min = 0.0
    leverage_hf_max = 4.0
    alpha_hf_div = 10
    leverage_hf_div = 10
    interval = 3
    simSize =5000
    
    hf_val = matrix( numpy.zeros((interval+1,simSize)) )
    mf_val = matrix( numpy.zeros((interval+1,simSize)) )
    if_val = matrix( numpy.zeros((interval+1,simSize)) )
    rf_val = matrix( numpy.zeros((interval+1,simSize)) )
    
    # Instantiate and initialize the Simulation parameters object
    simparamObj = SimulationParams.SimulationParams(hedgefund_val=hf_val,mutualfund_val=mf_val,indexfund_val=if_val,riskfree_val=rf_val);
    #-----Initialize object here----- the values should come from the request xml file          
    
    hfcoeff_hf_if_rf, ce_hf_minus_mf, hedgefund_val_interim = HfAlpha_LeverageIterator(simparamObj)
    # ----Define threads to invoke each iteration set required as per input from the user
    
    # Return the difference in certainty equivalence for HF-MF plotted against HF Alpha and HF Leverage    
    return ce_hf_minus_mf.tolist()
    
    # Temporary code for plot checking of output    
    #binCtrs = numpy.arange(0.0, 2.0, 0.05)
    #n = simparamObj.simSize
    #counts,bins = numpy.histogram(hedgefund_val_interim[0,:], bins = binCtrs )
    #binWidth = 0.7*(bins[1]-bins[0])
    #center = (bins[:-1]+bins[1:])/2 
    #plt.bar(center, counts, align = 'center', width = binWidth)
    #plt.show()
    
    #delta_alpha_hf = (simparamObj.alpha_hf_max - simparamObj.alpha_hf_min)/(alpha_hf_div)
    #delta_leverage_hf = (leverage_hf_max - leverage_hf_min)/(leverage_hf_div)
    
    #meshy = numpy.arange(simparamObj.alpha_hf_min, simparamObj.alpha_hf_max+delta_alpha_hf, delta_alpha_hf)
    #meshx = numpy.arange(simparamObj.leverage_hf_min, simparamObj.leverage_hf_max+delta_leverage_hf, delta_leverage_hf)
    #mX, mY = numpy.meshgrid(meshx,meshy)
    #fig = py.figure()
    #ax = p3.Axes3D(fig)
    #ax.contour3D(X,Y,Z)
    #ax.plot_wireframe(mX, mY, hfcoeff_hf_if_rf, rstride=1, cstride=1)
    #ax.set_ylabel('HF Alpha')
    #ax.set_xlabel('HF Leverage')
    #ax.set_zlabel('Initial Fraction of HF')
    #py.show()
    
    #Contour plot
    #plt.figure()
    #CS = plt.contour(mX, mY, ce_hf_minus_mf)
    #plt.clabel(CS, inline=1, fontsize=10)
    #plt.show()
    
#    print(hedgefund_val_interim)
#    print(out)
    
    
    
    
 
#if __name__ == "__main__":
#    calcHedgefundvalue()



