"""
Adiabatic flame temperature and equilibrium composition for a fuel/air mixture
as a function of equivalence ratio.
"""

import matplotlib.pyplot as plt
import cantera as ct
import numpy as np
import csv
import sys


gas = ct.Solution('gri30.yaml')

# equivalence ratio range
phi_min = 0.2
phi_max = 3.6
npoints = 35

# Set the gas composition :
T = 300.0
P = 101325.0

# find fuel, nitrogen, and oxygen indices
fuel_species = 'CH4'
ifuel = gas.species_index(fuel_species)
io2 = gas.species_index('O2')
in2 = gas.species_index('N2')

# air composition
air_N2_O2_ratio = 3.76
stoich_O2 = gas.n_atoms(fuel_species, 'C') + 0.25 * \
    gas.n_atoms(fuel_species, 'H')


# create some arrays to hold the data
phi = np.zeros(npoints)
tad = np.zeros(npoints)
xeq = np.zeros((gas.n_species, npoints))


for i in range(npoints):
    phi[i] = phi_min + (phi_max - phi_min)*i/(npoints - 1)
    X = np.zeros(gas.n_species)
    X[ifuel] = phi[i]
    X[io2] = stoich_O2
    X[in2] = stoich_O2*air_N2_O2_ratio

    # set the gas state
    gas.TPX = T, P, X

    # equilibrate the mixture adiabatically at constant P
    gas.equilibrate('HP')

    tad[i] = gas.T
    xeq[:, i] = gas.X
    print("At phi = ", "%10.4f" % (phi[i]) + "  Tad = ", "%10.4f" % (tad[i]))


# write output CSV file for importing into Excel
csv_file = 'adiabatic.csv'
with open(csv_file, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['phi', 'T (K)'] + gas.species_names)
    for i in range(npoints):
        writer.writerow([phi[i], tad[i]] + list(xeq[:, i]))
print(f'Output written to {0}'.format(csv_file))


# # Plot your results
# # The mass fractions of selected species
# if '--plot' in sys.argv:
#     import matplotlib.pyplot as plt
#     for i, cas in enumerate(gas.species_names):
#         if cas in ['O2', 'CO2', 'CO']:
#             plt.plot(phi, xeq[i, :], label=cas)
#             plt.hold(True)
#     plt.xlabel('Equivalence ratio')
#     plt.ylabel('Mass fractions')
#     plt.hold(False)
#     plt.legend(loc='best')
#     plt.savefig('plot.png', bbox_inches='tight')

# # The adiabatic flame temperature
# # plt.savefig('plot_flamespeed-'+str(tin)+'-'+str(p)+'.png', bbox_inches='tight')
# plt.plot(phi, tad)
# plt.xlabel('Equivalence ratio')
# plt.ylabel('Adiabatic flame temperature [K]')
# plt.show()
# plt.savefig('plot.png', bbox_inches='tight')
