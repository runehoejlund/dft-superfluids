import numpy as np
import matplotlib.pyplot as plt
from qeh import make_heterostructure, Heterostructure

# 1. Is this the correct way?? yes
# Also try without encapsulating (padding) in 3BN
layers = ['3BN', 'MoS2', '3BN', 'WSe2', '3BN']
hs = make_heterostructure(layers)

# Calculate screened potential W(q, \omega)
# 2. what is q, \omega?
# 3. Which layer?
W_MoS2 = hs.get_screened_potential(layer=3)
W_WSe2 = hs.get_screened_potential(layer=7)

# 4. What do we do with these (potentials calculated above)?

# 5. WHAT???!?!?!?!?!? 2*number of layers, first is spin up
# but electrons in BN-layers
# consider single electron in n-doped layer
# consider single hole in p-dopedlayer
hl_array = np.array([0., 0., 1., 0.])
el_array = np.array([1., 0., 0., 0.])

# Calculate exciton screened potential
W_MoS2 = hs.get_exciton_screened_potential(e_distr=el_array, h_distr=hl_array)
# 6. And what do we do with these (potentials calculated above)?

# 7. WHERE DO WE GET THE effective mass FROM?
inter_mass = 0.244

ee, ev = hs.get_exciton_binding_energies(eff_mass=inter_mass,
                                         e_distr=el_array,
                                         h_distr=hl_array)

print('The interlayer exciton binding energy is:', -ee[0])