#%%
import numpy as np
import matplotlib.pyplot as plt
from qeh import make_heterostructure, Heterostructure
from default_parameters import get_thickness, get_intermass
import ase.units

Hartree = ase.units.Hartree
Bohr = ase.units.Bohr

# Choose number of padding layers.
# Experiment with and without encapsulating (padding) in BN
nPadding=3
d_BN = 3.22  # hBN-hBN distance
d_MoS2 = get_thickness('H-MoS2')
d_MoS2_BN = (d_BN+d_MoS2)/2  # MoS2-hBN distance

d_WSe2 = get_thickness('H-WSe2')
d_WSe2_BN = (d_BN+d_WSe2)/2  # WSe2-hBN distance

d= [d_BN]*(nPadding-1) + [d_MoS2_BN]*2 + [d_BN]*(3-1) + [d_WSe2_BN]*2 + [d_BN]*(nPadding-1)

layers = ['{}BN'.format(nPadding), 'H-MoS2', '3BN', 'H-WSe2', '{}BN'.format(nPadding)]

# hs = make_heterostructure(layers)
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
plt.savefig('./plots/eps_VDWH_MoS2_WSe2.svg')
plt.close()
# plt.show()

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