# homogeneous equilibrium of a gas.

from cantera import *

# create an object representing the gas phase
gas = Solution('gri30.yaml')

# set the initial state
gas.TPX = 300.0, 1.0e05, 'CH4:0.5, O2:1, N2:3.76'

# equilibrate the gas holding T and P fixed
gas.equilibrate("HP")

# print a summary of the results
print(gas())