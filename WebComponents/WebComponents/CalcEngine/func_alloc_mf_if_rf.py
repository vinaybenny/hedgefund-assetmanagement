# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 15:31:57 2013
@author: VINAY

Function:  func_alloc_mf_if_rf()

Description: This function defines the allocation of wealth between mutual fund,
index fund and risk-free asset. This function, when minimized, gives the maximum wealth 
output, and the coefficients of allocation of each option that result in maximum wealth.


"""
# Imports numerical python packages
import numpy
from numpy import power


def func_alloc_mf_if_rf( coeffs, simparamObj, sign = -1.0  ):
        
        index_coeff = coeffs[0]         # Amount of initial wealth invested in index fund
        mutual_coeff = coeffs[1]         # Amount of initial wealth invested in mutual fund
        riskfree_coeff = simparamObj.initWealth - index_coeff - mutual_coeff #Remaining wealth is in the risk-free holdings
       
        # Define the wealth value using the input coefficients
        wealth_val = numpy.multiply(index_coeff,simparamObj.indexfund_val) + numpy.multiply(mutual_coeff,simparamObj.mutualfund_val) + \
        numpy.multiply(riskfree_coeff,simparamObj.riskfree_val)
        liquidation_wealth = simparamObj.liquidPercent*simparamObj.initWealth
            
        # Get the array indices of all those wealth values that dropped below the liquidation percentage
        #---Check with Prof if this is > or >=.
        rowindices, columnindices = numpy.nonzero(wealth_val <= liquidation_wealth)
        
        # Update all the elements in the last row of wealth_val, that have column indices specified in columnindices list.
        # This is to set those wealth values to the liquidation level.
        if numpy.size(columnindices) != 0:
            iter1 = numpy.nditer(columnindices)
            while not iter1.finished:
                wealth_val[simparamObj.interval,iter1] = liquidation_wealth
                iter1.iternext()
        # End of iter1 loop
        
        riskaver_param = 1-simparamObj.relriskAversion
        return sign * numpy.mean( power(wealth_val[simparamObj.interval,:], riskaver_param) / riskaver_param, dtype=numpy.float64)