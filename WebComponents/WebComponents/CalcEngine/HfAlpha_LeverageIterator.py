'''
Created on Nov 27, 2013

@author: VINAY

Function:  HfAlpha_LeverageIterator()

Description: This function will produce the contour plot matrix for the HF Alpha versus the HF Leverage. The function will be called
as a thread from the main program.

Input: SimulationParams Object
Output: 
'''

import numpy
from numpy import matrix
from scipy.optimize import minimize

from func_alloc_hf_if_rf import func_alloc_hf_if_rf
from func_alloc_mf_if_rf import func_alloc_mf_if_rf
from func_alloc_hf_mf_if_rf import func_alloc_hf_mf_if_rf
from func_ieq_constraints import f_ieqcon_hf_if_rf, f_ieqcon_mf_if_rf, f_ieqcon_hf_mf_if_rf


def HfAlpha_LeverageIterator(simparamObj ):
    "This section is for the production of alpha_hf to leverage contour plot"
    
    # Extract simulation specifications  
    alpha_hf_min = simparamObj.alpha_hf_min
    alpha_hf_max = simparamObj.alpha_hf_max
    alpha_hf_div = simparamObj.alpha_hf_div
    
    leverage_hf_min = simparamObj.leverage_hf_min
    leverage_hf_max = simparamObj.leverage_hf_max
    leverage_hf_div = simparamObj.leverage_hf_div    
    
    # 2D Arrays for optimal coefficients, maximum wealth for each input value of alpha and leverage 
    ifcoeff_hf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))  
    hfcoeff_hf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))
    fx_hf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))
    
    ifcoeff_mf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))  
    mfcoeff_mf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))
    fx_mf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))
    
    ifcoeff_hf_mf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))
    mfcoeff_hf_mf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))
    hfcoeff_hf_mf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))
    fx_hf_mf_if_rf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))
    
    # 2D array for certainty equivalence difference between hedge and mutual funds 
    ce_hf_minus_mf = numpy.zeros((alpha_hf_div+1,leverage_hf_div+1))
    
    # Define Weiner Process matrix and populate it with Std Normal Distribution
    weiner_hf = matrix(numpy.random.randn(simparamObj.interval,simparamObj.simSize))
    weiner_if = matrix(numpy.random.randn(simparamObj.interval,simparamObj.simSize))
    weiner_mf = matrix(numpy.random.randn(simparamObj.interval,simparamObj.simSize))
    
    # Code to read the weiner martices from file -For testing and comparison
#    weiner_hf = genfromtxt("w_h.csv", dtype=numpy.float64, delimiter=',')
#    weiner_if = genfromtxt("w_i.csv", dtype=numpy.float64, delimiter=',')
#    weiner_mf = genfromtxt("w_m.csv", dtype=numpy.float64, delimiter=',')
    
    # Define hedge fund temporary matrix that holds the current time iteration value of HF   
    hedgefund_val_interim = matrix( numpy.ones((1, simparamObj.simSize)) )
    zeromat = matrix(numpy.zeros((1, simparamObj.simSize)))
    onemat = matrix(numpy.ones((1, simparamObj.simSize)))
    
    # Define the delta increases in alpha_hf and leverage_hf for each instance of looping    
    delta_alpha_hf = (alpha_hf_max - alpha_hf_min)/alpha_hf_div
    alpha_hf = alpha_hf_min
    delta_leverage_hf = (leverage_hf_max - leverage_hf_min)/leverage_hf_div
    
    # Optimizing the loop calculations- Define temporary variables for quantities that are loop invariant.    
    time_interval = float(simparamObj.timeHorizon) / float(simparamObj.interval)
    time_interval_sqrt_init = numpy.sqrt(time_interval)
    hedgefund_val_init = (1 - simparamObj.fundManagefee_hf)**simparamObj.timeHorizon
    mutualfund_init = (1 - simparamObj.fundManagefee_mf)**simparamObj.timeHorizon
    expterm1_hf_mean_init = simparamObj.mktriskPrice*simparamObj.beta*simparamObj.volatility_if
    expterm1_hf_var_init = 0.5*((simparamObj.beta*simparamObj.volatility_if)**2 + simparamObj.volatility_hf**2)
    expterm2_hf_nondeter_init = numpy.add(numpy.multiply(simparamObj.beta*simparamObj.volatility_if, weiner_if) , \
                numpy.multiply(simparamObj.volatility_hf, weiner_hf))* time_interval_sqrt_init
    riskfree_val_init = numpy.exp(simparamObj.riskfreeRate*time_interval)
    expterm1_if = (simparamObj.riskfreeRate+(simparamObj.mktriskPrice*simparamObj.volatility_if) - \
                (0.5*(simparamObj.volatility_if**2))  )*time_interval
    expterm2_if = numpy.multiply((simparamObj.volatility_if*time_interval_sqrt_init), weiner_if)
    indexfund_val_init = numpy.exp(numpy.add(expterm1_if,expterm2_if))
    expterm1_mf = (simparamObj.riskfreeRate+(simparamObj.mktriskPrice*simparamObj.volatility_ifmf + \
                simparamObj.alpha_mf) - 0.5*(simparamObj.volatility_ifmf**2 + \
                simparamObj.volatility_mf**2))* time_interval
    expterm2_mf = numpy.add(numpy.multiply(simparamObj.volatility_ifmf, weiner_if), \
                numpy.multiply(simparamObj.volatility_mf, weiner_mf))* time_interval_sqrt_init
    mutualfund_val_init = numpy.exp(numpy.add(expterm1_mf,expterm2_mf))
    bounds_init = (1+simparamObj.maxLeverage)*simparamObj.initWealth
    riskaver_param = 1-simparamObj.relriskAversion
    inv_riskaver_param = 1/riskaver_param
    ce_hf_mf_multiplier = (riskaver_param**inv_riskaver_param)/simparamObj.initWealth
    
    
    # Number of iterations for alpha values should be the (Number of divisions + 1)
    for iter1 in range(alpha_hf_div+1):
        leverage_hf = leverage_hf_min 
        
        # Number of iterations for leverage values should be the (Number of divisions + 1)
        for iter2 in range(leverage_hf_div+1):
            
            # Initialize the values for hedge fund, mutual fund, index fund and risk-free for every combination of leverage_hf and alpha_hf           
            hedgefund_val_interim[0,:] = hedgefund_val_init
            simparamObj.hedgefund_val[0,:] = hedgefund_val_init
            simparamObj.riskfree_val[0,:] = 1
            simparamObj.indexfund_val[0.:] = 1
            simparamObj.mutualfund_val[0,:].fill(mutualfund_init)
               
            for iter3 in range(simparamObj.interval):
                                
                # Deterministic section of governing equation - HF value
                expterm1_hf = (simparamObj.riskfreeRate+(1+leverage_hf)* \
                (expterm1_hf_mean_init + alpha_hf) - expterm1_hf_var_init*(1+leverage_hf)**2) * time_interval
                
                # Nondeterministic Brownian motion section of governing equation- HF value
                expterm2_hf = (1+leverage_hf)*expterm2_hf_nondeter_init[iter3,:]
                
                
                # Put deterministic and nondeterministic parts together- HF value for the current time slice
                hedgefund_val_interim[0,:] = numpy.multiply(hedgefund_val_interim[0,:] ,numpy.exp(numpy.add(expterm1_hf,expterm2_hf)) )
                
                # Store the current time slice value of HF into the next row of the hedgefund value matrix                
                simparamObj.hedgefund_val[iter3+1,:] = numpy.subtract( hedgefund_val_interim[0,:] , \
                simparamObj.performFee_hf*numpy.maximum(hedgefund_val_interim[0,:]-onemat[0,:],zeromat[0,:]) )
                
                #Calculate value of risk-free for current time slice and store into next row of the risk-free value matrix
                simparamObj.riskfree_val[iter3+1,:] = numpy.multiply( simparamObj.riskfree_val[iter3,:], riskfree_val_init )
                
                # Deterministic section of governing equation - IF value
                "Moved to outside the loop as part of loop optimization"                
                
                
                # Nondeterministic Brownian motion section of governing equation- IF value
                "Moved to outside the loop as part of loop optimization"
                
                
                # Calculate value of index fund for current time slice and store into next row of the indexfund value matrix                
                simparamObj.indexfund_val[iter3+1,:] = numpy.multiply(simparamObj.indexfund_val[iter3,:], indexfund_val_init[iter3,:] )             
                
                # Deterministic section of governing equation - MF value
                "Moved to outside the loop as part of loop optimization"
                
                # Nondeterministic Brownian motion section of governing equation- MF value
                "Moved to outside the loop as part of loop optimization"                
                
                # Calculate value of mutual fund for current time slice and store into next row of the mutualfund value matrix                
                simparamObj.mutualfund_val[iter3+1,:] = numpy.multiply(simparamObj.mutualfund_val[iter3,:], mutualfund_val_init[iter3,:] )                
                
                # End of iter3 loop
            
            init_guess = [0.0, 0.0]
            init_guess_all = [0., 0., 0.]

            # Define the constraints and maximize the wealth function for HF-IF scenario 
 
            cons_hf_if_rf = ({'type': 'ineq',\
                    'fun': f_ieqcon_hf_if_rf,\
                    'args': (simparamObj,1.0) }
                    )
            out_hf_if_rf = minimize(func_alloc_hf_if_rf, init_guess, constraints=cons_hf_if_rf, args=(simparamObj,), \
            bounds = [(0. ,bounds_init),(0. , bounds_init)],method='SLSQP', options={'disp': False})
            
            ifcoeff_hf_if_rf[iter1,iter2] = out_hf_if_rf.x[0]       # index fraction for HF-IF case
            hfcoeff_hf_if_rf[iter1,iter2] = out_hf_if_rf.x[1]       # hedge fraction for MF-IF case
            fx_hf_if_rf[iter1,iter2] = out_hf_if_rf.fun             # Max wealth for HF-IF case 
            
            # Maximize the wealth function for MF-IF scenario       
            cons_mf_if_rf = ({'type': 'ineq',\
                    'fun': f_ieqcon_mf_if_rf,\
                    'args': (simparamObj,1.0) }
                    )
            out_mf_if_rf = minimize(func_alloc_mf_if_rf, init_guess, constraints=cons_mf_if_rf, args=(simparamObj,), \
            bounds = [(0. ,bounds_init),(0. , bounds_init)],method='SLSQP', options={'disp': False})
            
            ifcoeff_mf_if_rf[iter1,iter2] = out_mf_if_rf.x[0]      # index fraction for MF-IF case
            mfcoeff_mf_if_rf[iter1,iter2] = out_mf_if_rf.x[1]      # mutual fraction for MF-IF case
            fx_mf_if_rf[iter1,iter2] = out_mf_if_rf.fun            # Max wealth for MF-IF case            
            
            
            # Maximize the wealth function for HF-MF-IF scenario
            cons_hf_mf_if_rf = ({'type': 'ineq',\
                    'fun': f_ieqcon_hf_mf_if_rf,\
                    'args': (simparamObj,1.0) }
                    )            
            out_hf_mf_if_rf = minimize(func_alloc_hf_mf_if_rf, init_guess_all, constraints=cons_hf_mf_if_rf, args=(simparamObj,), \
            bounds = [(0. ,bounds_init),(0. , bounds_init), (0. , bounds_init)],method='SLSQP', options={'disp': False})
            
            ifcoeff_hf_mf_if_rf[iter1,iter2] = out_hf_mf_if_rf.x[0]    # index fraction for HF-MF-IF case
            mfcoeff_hf_mf_if_rf[iter1,iter2] = out_hf_mf_if_rf.x[1]    # mutual fraction for HF-MF-IF case
            hfcoeff_hf_mf_if_rf[iter1,iter2] = out_hf_mf_if_rf.x[2]    # hedge fraction for HF-MF-IF case
            fx_hf_mf_if_rf[iter1,iter2] = out_hf_mf_if_rf.fun          # Max wealth for HF-MF-IF case
            
#            # Certainty Equivalence relation between Hedge fund and Mutual fund
            ce_hf_minus_mf[iter1, iter2] =  -ce_hf_mf_multiplier * ( (fx_hf_if_rf[iter1,iter2]**inv_riskaver_param) - \
            (fx_mf_if_rf[iter1,iter2]**inv_riskaver_param) )  
            
            print("iter1: "+repr(iter1)+" iter2: "+repr(iter2) )
            leverage_hf = leverage_hf + delta_leverage_hf
            # End of iter2 loop                         
        
        alpha_hf = alpha_hf + delta_alpha_hf
        # End of iter1 loop
    
    return hfcoeff_hf_if_rf, ce_hf_minus_mf, hedgefund_val_interim
    