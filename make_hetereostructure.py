import numpy as np
import matplotlib.pyplot as plt
from qeh import make_heterostructure, Heterostructure

#choose number of padding layers
nPadding=3

# 1. Is this the correct way?? yes
# Also try without encapsulating (padding) in 3BN
layers = ['{}BN'.format(nPadding), 'MoS2', '3BN', 'WSe2', '{}BN'.format(nPadding)]
hs = make_heterostructure(layers)

# Calculate screened potential W(q, \omega)
# 2. what is q, \omega?
# 3. Which layer?
W_MoS2 = hs.get_screened_potential(layer=nPadding)
W_WSe2 = hs.get_screened_potential(layer=nPadding+4)

# 4. What do we do with these (potentials calculated above)?

# 5.
# 2*number of layers, first is spin up
# but no electrons in BN-layers
# consider single electron in n-doped layer
# consider single hole in p-dopedlayer
zeroPadding=np.zeros(2*nPadding)
hl_array = np.hstack([zeroPadding, np.array([1., 0.]), np.zeros(6), np.array([0., 0.]),zeroPadding ])
el_array = np.hstack([zeroPadding, np.array([0., 0.]), np.zeros(6), np.array([1., 0.]),zeroPadding ])

# Calculate exciton screened potential
W_MoS2 = hs.get_exciton_screened_potential(e_distr=el_array, h_distr=hl_array)
# 6. And what do we do with these (potentials calculated above)?

# 7. WHERE DO WE GET THE effective mass FROM?
# 1/m*=1/me*+1/mh* - me* and mh* can be found in c2db
inter_mass = 0.244

ee, ev = hs.get_exciton_binding_energies(eff_mass=inter_mass,
                                         e_distr=el_array,
                                         h_distr=hl_array)

print('The interlayer exciton binding energy is:', -ee[0])