# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 17:53:23 2013

@author: VINAY
"""

class SimulationParams:
    'Base Class that has all the necessary parameters for running simulations'
        
    # Override the init method for initializing an object of this class
    def __init__(self,\
    hedgefund_val,\
    mutualfund_val,\
    indexfund_val,\
    riskfree_val,\
    
    initWealth = 1.,\
    relriskAversion = 2,\
    timeHorizon = 1,\
    riskfreeRate = 0.03,\
    mktriskPrice = 0.05,\
    liquidPercent = 0.02,\
    maxLeverage = 1.,\
    alpha_hf = 0.08,\
    fundManagefee_hf = 0.02,\
    performFee_hf = 0.2,\
    leverage_hf = 1.,\
    volatility_hf = 0.1,\
    beta=0,\
    fundManagefee_mf = 0.01,\
    alpha_mf = 0.02,\
    volatility_ifmf = 0.2,\
    volatility_mf = 0.06,\
    volatility_if = 0.2,
    jump_size = 0.0,\
    
    # Simulation and Range Parameters
    interval = 3,\
    simSize = 5000,\
    alpha_hf_min = 0.0,\
    alpha_hf_max = 0.08,\
    alpha_hf_div = 10,\
    alpha_mf_min = 0.0,\
    alpha_mf_max = 0.08,\
    alpha_mf_div = 30,\
    leverage_hf_min = 0.0,\
    leverage_hf_max = 4.0,\
    leverage_hf_div = 10,\
    performFee_hf_min = 0.,\
    performFee_hf_max = 0.5,\
    performFee_hf_div = 30,\
    volatility_hf_min = 0.,\
    volatility_hf_max = 0.25,\
    volatility_hf_div = 30,\
    volatility_ifmf_min = 0.,\
    volatility_ifmf_max = 0.25,\
    volatility_ifmf_div = 30,\
    beta_min = 0,\
    beta_max = 1,\
    beta_div = 30    
    ):
        
        #Define the values of the main parameters
    
        # General variables
        self.initWealth = initWealth            # Initial wealth
        self.relriskAversion = relriskAversion   # Coefficient of Relative Risk Aversion
        self.timeHorizon = timeHorizon          # Time horizon for the calculation(in years)
        self.riskfreeRate = riskfreeRate        # Risk-free rate
        self.mktriskPrice = mktriskPrice         # Market price of Risk  
        self.liquidPercent = liquidPercent      # Cut-off percentage of wealth for liquidation
        self.maxLeverage = maxLeverage          # The maximum leverage limit. Hence the total wealth available for investing in case of Hedge funds would be ( initWealth + L*initWealth)       
        
        # Hedge fund related variables
        self.hedgefund_val = hedgefund_val          # Hedge fund value matrix( K+1 * simSize ). Last row gives the final values at the end of the time interval for all simulation outcomes
        self.alpha_hf = alpha_hf                    # Hedge fund alpha (before fees)
        self.fundManagefee_hf = fundManagefee_hf    # Hedge fund management fee
        self.performFee_hf = performFee_hf          # Hedge fund performance fee: 20%
        self.leverage_hf = leverage_hf              # Hedge fund leverage
        self.volatility_hf = volatility_hf          # Second Hedge fund volatility component
        self.beta = beta                            # First hedge fund volatility component (market component in unlevered portfolio)
        
        # Mutual fund related variables
        self.mutualfund_val = mutualfund_val            # Mutual fund value matrix. fund value matrix. Configuration same as above.
        self.fundManagefee_mf = fundManagefee_mf        # Active fund management fee
        self.alpha_mf = alpha_mf                        # Mutual fund alpha (before fees)
        self.volatility_ifmf = volatility_ifmf          # First mutual fund volatility component
        self.volatility_mf = volatility_mf              # Second mutual fund volatility component (pure active component)
        
        # Index fund related variables
        self.indexfund_val = indexfund_val      # Index fund value matrix. Configuration same as above.
        self.volatility_if = volatility_if      # Index fund (ie, market) volatility
        
        # Risk-free assets related variables
        self.riskfree_val = riskfree_val        # Risk-free asset value matrix. Configuration same as above.
        
        # Jump Size
        self.jump_size = jump_size              # Mean jump size (negative jumps) if the user chooses a stochastic jump

        # Range variables         
        self.interval = interval                # Monitoring intervals at which wealth needs to be calculated, to check whether liquidation needs to be performed.
        self.simSize = simSize                  # Total number of outcomes to be simulated        
        self.alpha_hf_min = alpha_hf_min
        self.alpha_hf_max = alpha_hf_max
        self.alpha_hf_div = alpha_hf_div
        self.alpha_mf_min = alpha_mf_min
        self.alpha_mf_max = alpha_mf_max
        self.alpha_mf_div = alpha_mf_div
        self.leverage_hf_min = leverage_hf_min
        self.leverage_hf_max = leverage_hf_max
        self.leverage_hf_div = leverage_hf_div
        self.performFee_hf_min = performFee_hf_min
        self.performFee_hf_max = performFee_hf_max
        self.performFee_hf_div = performFee_hf_div
        self.volatility_hf_min = volatility_hf_min
        self.volatility_hf_max = volatility_hf_max
        self.volatility_hf_div = volatility_hf_div
        self.volatility_ifmf_min = volatility_ifmf_min
        self.volatility_ifmf_max = volatility_ifmf_max
        self.volatility_ifmf_div = volatility_ifmf_div
        self.beta_min = beta_min
        self.beta_max = beta_max
        self.beta_div = beta_div
    
    
    
    
    
    
    
    
    
    
    
    
    
    