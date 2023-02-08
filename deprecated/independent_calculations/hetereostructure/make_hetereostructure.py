#%%
import numpy as np
import matplotlib.pyplot as plt
from default_parameters import get_thickness, get_intermass
import ase.units
from gpaw import GPAW
from gpaw.response.qeh import interpolate_building_blocks
from qeh import make_heterostructure, Heterostructure

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

Hartree = ase.units.Hartree
Bohr = ase.units.Bohr

# Choose number of padding layers.
# Experiment with and without encapsulating (padding) in BN
nPadding=3
p = 'WS2'
Hp = 'H-' + p
n = 'WSe2'
Hn = 'H-' + n

d_BN = 3.22  # hBN-hBN distance
d_p = get_thickness(Hp)
d_p_BN = (d_BN+d_p)/2  # (p-doped) TMD - hBN distance
d_n = get_thickness(Hn)
d_n_BN = (d_BN+d_n)/2  # (n-doped) TMD - hBN distance


layers = ['{}BN'.format(nPadding), p, '3BN', n, '{}BN'.format(nPadding)]
layers = [l + '_int' for l in layers]

d = [d_BN]*(nPadding-1) + [d_p_BN]*2 + [d_BN]*(3-1) + [d_n_BN]*2 + [d_BN]*(nPadding-1)

# # layers = [p + '_int', 'BN_int', 'BN_int', 'BN_int', n + '_int']
# # d = [d_p_BN]*(len(layers) - 1)

hs = Heterostructure(structure=layers,  # set up structure
                        d=d,                         # layer distance array
                        include_dipole=True,
                        wmax=0,                      # only include \omega=0
                        qmax=1,                      # q grid up to 1 Ang^{-1}
                        d0=0)                     # width of single layer (only used for monolayer calculation), so currently set to 0

# %%
# # Get Macroscropic Dielectric function
q, w, epsM = hs.get_macroscopic_dielectric_function()
plt.plot(q, epsM.real)
plt.xlim(0, 1)
plt.xlabel(r'$q_\parallel (\mathrm{\AA^{-1}}$)', fontsize=20)
plt.ylabel(r'$\epsilon_M(q, \omega=0)$', fontsize=20)
plt.title('Static dielectric function', fontsize=20)
plt.legend(ncol=2, loc='best')
plt.savefig('./plots/eps_VDWH_p=' + p + '_n=' + n + '.svg')
plt.show()
plt.close()

# %%
# Calculate screened potential W(q, \omega)
# 2. what is q, \omega?
# 3. Which layer?
W_MoS2 = hs.get_screened_potential(layer=nPadding)
W_WSe2 = hs.get_screened_potential(layer=nPadding+4)
q = hs.q_abs / Bohr # get q-array (momentum transfer range) in Ångstrom.

# plt.plot(q[1:], W_MoS2[1:,].real)
# plt.xlim(0, 1)
# plt.xlabel(r'$q_\parallel (\mathrm{\AA^{-1}}$)', fontsize=20)
# plt.ylabel(r'$W_{\mathrm{MoS_2}}(q, \omega=0)$', fontsize=20)
# plt.title('Screened potential in MoS2-layer', fontsize=20)
# plt.show()

# plt.plot(q[1:], W_WSe2[1:,].real)
# plt.xlim(0, 1)
# plt.xlabel(r'$q_\parallel (\mathrm{\AA^{-1}}$)', fontsize=20)
# plt.ylabel(r'$W_{\mathrm{WSe_2}}(q, \omega=0)$', fontsize=20)
# plt.title('Screened potential in WSe2-layer', fontsize=20)
# plt.show()

# plot together
plt.plot(q[1:], W_MoS2[1:,].real)
plt.plot(q[1:], W_WSe2[1:,].real,'--')
# plt.xlim(0, 1)
plt.xlabel(r'$q_\parallel (\mathrm{\AA^{-1}}$)', fontsize=20)
plt.ylabel(r'$U}(q, \omega=0)$', fontsize=20)
plt.title('Screened potential', fontsize=20)
plt.legend(['MoS2','WSe2'])
plt.savefig('./plots/W_VDWH_MoS2_WSe2.svg')
# plt.show()
# # 4. What do we do with these (potentials calculated above)?

# %%
# Plot exciton screened potential
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

# The effective interlayer exciton mass is calculated as:
# 1/m*=1/me*+1/mh*.
# me* and mh* can be found in c2db,
# but we import them from the default_parameters.py.
ee, ev = hs.get_exciton_binding_energies(eff_mass=get_intermass('H-WSe2', 'H-MoS2'),
                                         e_distr=el_array,
                                         h_distr=hl_array)

print('The interlayer exciton binding energy is: {:0.4f} eV'.format(-ee[0].real))