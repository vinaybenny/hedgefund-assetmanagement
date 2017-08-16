from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from WebComponents.CalcEngine import calculateHedgefundvalue
from tastypie.utils.timezone import now
import cPickle
import json
import httplib


class UserInformation(models.Model):
    userName = models.CharField(max_length=200, blank=True, null=True)
    
    

class SimulationModel(models.Model):
    'Base Class that has all the necessary parameters for running simulations. This is the structure of the table containing all simulations'
    #Define the values of the main parameters
    
    # User ID as the foreign key for identifying the user running the simulation
    user = models.ForeignKey(User)
    simType = models.IntegerField()
    simRequestTime = models.DateTimeField(default=now)

    # General variables
    initWealth = models.DecimalField(max_digits=30, decimal_places=15, default=1.0)             # Initial wealth
    relriskAversion = models.IntegerField(default=2)                             # Coefficient of Relative Risk Aversion
    timeHorizon = models.DecimalField(max_digits=30, decimal_places=15, default=1.0)       # Time horizon for the calculation(in years)
    riskfreeRate = models.DecimalField(max_digits=30, decimal_places=15, default=0.03)        # Risk-free rate
    mktriskPrice = models.DecimalField(max_digits=30, decimal_places=15, default=0.05)          # Market price of Risk  
    liquidPercent = models.DecimalField(max_digits=30, decimal_places=15, default=0.02)       # Cut-off percentage of wealth for liquidation
    maxLeverage = models.DecimalField(max_digits=30, decimal_places=15, default=1.0)           # The maximum leverage limit. Hence the total wealth available for investing in case of Hedge funds would be ( initWealth + L*initWealth)       
        
    # Hedge fund related variables
    alpha_hf = models.DecimalField(max_digits=30, decimal_places=15, default=0.08)                    # Hedge fund alpha (before fees)
    fundManagefee_hf = models.DecimalField(max_digits=30, decimal_places=15, default=0.02)    # Hedge fund management fee
    performFee_hf = models.DecimalField(max_digits=30, decimal_places=15, default=0.2)          # Hedge fund performance fee: 20%
    leverage_hf = models.DecimalField(max_digits=30, decimal_places=15, default=1.0)              # Hedge fund leverage
    volatility_hf = models.DecimalField(max_digits=30, decimal_places=15, default=0.1)          # Second Hedge fund volatility component
    beta = models.DecimalField(max_digits=30, decimal_places=15, default=0.0)                            # First hedge fund volatility component (market component in unlevered portfolio)
        
    # Mutual fund related variables
    fundManagefee_mf = models.DecimalField(max_digits=30, decimal_places=15, default=0.01)        # Active fund management fee
    alpha_mf = models.DecimalField(max_digits=30, decimal_places=15, default=0.02)                        # Mutual fund alpha (before fees)
    volatility_ifmf = models.DecimalField(max_digits=30, decimal_places=15, default=0.2)          # First mutual fund volatility component
    volatility_mf = models.DecimalField(max_digits=30, decimal_places=15, default=0.06)              # Second mutual fund volatility component (pure active component)
        
    # Index fund related variables
    volatility_if = models.DecimalField(max_digits=30, decimal_places=15, default=0.2)      # Index fund (ie, market) volatility
    
    # Jump Parameters
    jump_size = models.DecimalField(max_digits=30, decimal_places=15, default=0.0)
           
    # Range variables         
    interval = models.IntegerField(default=3)                # Monitoring intervals at which wealth needs to be calculated, to check whether liquidation needs to be performed.
    simSize = models.IntegerField(default=5000)                   # Total number of outcomes to be simulated        
    alpha_hf_min = models.DecimalField(max_digits=30, decimal_places=15, default=0.00)
    alpha_hf_max = models.DecimalField(max_digits=30, decimal_places=15, default=0.08)
    alpha_hf_div = models.IntegerField(default=10)
    alpha_mf_min = models.DecimalField(max_digits=30, decimal_places=15, default=0.00)
    alpha_mf_max = models.DecimalField(max_digits=30, decimal_places=15, default=0.08)
    alpha_mf_div = models.IntegerField(default=10)
    leverage_hf_min = models.DecimalField(max_digits=30, decimal_places=15, default=0.00)
    leverage_hf_max = models.DecimalField(max_digits=30, decimal_places=15, default=4.00)
    leverage_hf_div = models.IntegerField(default=10)
    performFee_hf_min = models.DecimalField(max_digits=30, decimal_places=15, default=0.00)
    performFee_hf_max = models.DecimalField(max_digits=30, decimal_places=15, default=0.50)
    performFee_hf_div = models.IntegerField(default=10)
    volatility_hf_min = models.DecimalField(max_digits=30, decimal_places=15, default=0.00)
    volatility_hf_max = models.DecimalField(max_digits=30, decimal_places=15, default=0.25)
    volatility_hf_div = models.IntegerField(default=10)
    volatility_ifmf_min = models.DecimalField(max_digits=30, decimal_places=15, default=0.00)
    volatility_ifmf_max = models.DecimalField(max_digits=30, decimal_places=15, default=0.25)
    volatility_ifmf_div = models.IntegerField(default=10)
    beta_min = models.DecimalField(max_digits=30, decimal_places=15, default=0.00)
    beta_max = models.DecimalField(max_digits=30, decimal_places=15, default=1.00)
    beta_div = models.IntegerField(default=10)

    def __unicode__(self):
        return unicode(self.id)


class SimulationResult(models.Model):
    simInstancekey = models.OneToOneField(SimulationModel)
    simResultarray = models.TextField()
    simResultTime = models.DateTimeField(default=now)


    def __unicode__(self):
        return unicode(self.id)
