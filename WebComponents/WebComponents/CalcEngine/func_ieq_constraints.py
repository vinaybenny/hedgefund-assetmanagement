'''
Created on Nov 27, 2013

@author: VINAY

Description: This file defines all the constraint functions subject to which the minimization of objective function
will be performed to maximize final investor wealth.
'''

import numpy

# Constraint function for hedge fund-index fund optimization scenario
def f_ieqcon_hf_if_rf(coeffs, simparamObj, sign=1.0):
        """ Inequality constraint, which states Wi(0)+Wh(0) <= (L+1)*W(0)"""
        return numpy.array([ sign*((1+simparamObj.maxLeverage)*simparamObj.initWealth-coeffs[0]-coeffs[1] ) ])

# Constraint function for mutual fund-index fund optimization scenario        
def f_ieqcon_mf_if_rf(coeffs, simparamObj, sign=1.0):
        """ Inequality constraint """
        return numpy.array([ sign*((1+simparamObj.maxLeverage)*simparamObj.initWealth-coeffs[0]-coeffs[1]) ])

# Constraint function for hedge fund-index fund-mutual fund optimization scenario        
def f_ieqcon_hf_mf_if_rf(coeffs, simparamObj, sign=1.0):
        """ Inequality constraint """
        return numpy.array([ sign*((1+simparamObj.maxLeverage)*simparamObj.initWealth-coeffs[0]-coeffs[1]-coeffs[2]) ])
    
