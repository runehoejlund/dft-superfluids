import numpy as np
from qeh import Heterostructure
from default_parameters import get_thickness, get_intermass
import ase.units

Hartree = ase.units.Hartree
Bohr = ase.units.Bohr

# %% HElPER FUNCTIONS FROM GPAW
import pickle
def load(fd):
    try:
        return pickle.load(fd, encoding='latin1')
    except TypeError:
        return pickle.load(fd)

def get_exciton_screened_potential_r(self, r_array, e_distr=None,
                                         h_distr=None, Wq_name=None,
                                         tweak=None):
        if Wq_name is not None:
            q_abs, W_q = load(open(Wq_name, 'rb'))
        else:
            q_temp, W_q, xxx = self.get_exciton_screened_potential(e_distr,
                                                                   h_distr)
 
        from scipy.special import jn

        inter = False
        if np.where(e_distr == 1)[0][0] != np.where(h_distr == 1)[0][0]:
            inter = True

        layer_dist = 0.
        if self.n_layers == 1:
            layer_thickness = self.s[0]
        else:
            if len(e_distr) == self.n_layers:
                div = 1
            else:
                div = 2

            if not inter:
                ilayer = np.where(e_distr == 1)[0][0] // div
                if ilayer == len(self.d):
                    ilayer -= 1
                layer_thickness = self.d[ilayer]
            else:
                ilayer1 = np.min([np.where(e_distr == 1)[0][0],
                                  np.where(h_distr == 1)[0][0]]) // div
                ilayer2 = np.max([np.where(e_distr == 1)[0][0],
                                  np.where(h_distr == 1)[0][0]]) // div
                layer_thickness = self.d[ilayer1] / 2.
                layer_dist = np.sum(self.d[ilayer1:ilayer2]) / 1.8
        if tweak is not None:
            layer_thickness = tweak

        W_q *= q_temp
        q = np.linspace(q_temp[0], q_temp[-1], 10000)
        Wt_q = np.interp(q, q_temp, W_q)
        Dq_Q2D = q[1] - q[0]

        if not inter:
            Coulombt_q = (-4. * np.pi / q *
                          (1. - np.exp(-q * layer_thickness / 2.)) /
                          layer_thickness)
        else:
            Coulombt_q = (-2 * np.pi / q *
                          (np.exp(-q * (layer_dist - layer_thickness / 2.)) -
                           np.exp(-q * (layer_dist + layer_thickness / 2.))) /
                          layer_thickness)

        W_r = np.zeros(len(r_array))
        for ir in range(len(r_array)):
            J_q = jn(0, q * r_array[ir])
            if r_array[ir] > np.exp(-13):
                Int_temp = (
                    -1. / layer_thickness *
                    np.log((layer_thickness / 2. - layer_dist +
                            np.sqrt(r_array[ir]**2 +
                                    (layer_thickness / 2. - layer_dist)**2)) /
                           (-layer_thickness / 2. - layer_dist +
                            np.sqrt(r_array[ir]**2 +
                                    (layer_thickness / 2. + layer_dist)**2))))
            else:
                if not inter:
                    Int_temp = (-1. / layer_thickness *
                                np.log(layer_thickness**2 / r_array[ir]**2))
                else:
                    Int_temp = (-1. / layer_thickness *
                                np.log((layer_thickness + 2 * layer_dist) /
                                       (2 * layer_dist - layer_thickness)))

            W_r[ir] = (Dq_Q2D / 2. / np.pi *
                       np.sum(J_q * (Wt_q - Coulombt_q)) +
                       Int_temp)

        return r_array, W_r

# %% CRUCIAL FUNCTION WHICH WE SHOULD IMPLEMENT
def get_exciton_binding_energies_coulomb(hs, eff_mass, L_min=-50, L_max=10,
                                     Delta=0.1, e_distr=None, h_distr=None,
                                     Wq_name=None, tweak=None):
                                     
        from scipy.linalg import eig
        r_space = np.arange(L_min, L_max, Delta)
        Nint = len(r_space)
        
        # EDIT THIS
        r, W_r = hs.get_exciton_screened_potential_r(r_array=np.exp(r_space),
                                                       e_distr=e_distr,
                                                       h_distr=h_distr,
                                                       Wq_name=None,
                                                       tweak=tweak)

        H = np.zeros((Nint, Nint), dtype=complex)
        for i in range(0, Nint):
            r_abs = np.exp(r_space[i])
            H[i, i] = - 1. / r_abs**2 / 2. / eff_mass \
                * (-2. / Delta**2 + 1. / 4.) + W_r[i]
            if i + 1 < Nint:
                H[i, i + 1] = -1. / r_abs**2 / 2. / eff_mass \
                    * (1. / Delta**2 - 1. / 2. / Delta)
            if i - 1 >= 0:
                H[i, i - 1] = -1. / r_abs**2 / 2. / eff_mass \
                    * (1. / Delta**2 + 1. / 2. / Delta)

        ee, ev = eig(H)
        index_sort = np.argsort(ee.real)
        ee = ee[index_sort]
        ev = ev[:, index_sort]
        return ee * Hartree, ev

# %% OUR OWN FUNCTIONS
def get_E_b_for_hs(hs, e_layer, h_layer, nFilling, nPadding):
    '''
    @returns: E_b
    '''
    Hartree = ase.units.Hartree
    Bohr = ase.units.Bohr

    # Exciton Screened Potential
    e_distr = np.array([0, 0]*nPadding + [0, 0] + [0, 0]*nFilling + [1, 0] + [0,0]*nPadding)
    h_distr = np.array([0, 0]*nPadding + [1, 0] + [0, 0]*nFilling + [0, 0] + [0,0]*nPadding)

    # Exciton Binding Energies
    ee, ev = hs.get_exciton_binding_energies(eff_mass=get_intermass('H-' + e_layer, 'H-' + h_layer),
                                            e_distr=e_distr,
                                            h_distr=h_distr)
    
    # TODO: This is where we sohuld use our own function also
    # ee_2d_coulomb, ev_2d_coullomb = get_exciton_binding_energies_coulomb(...)
    
    E_b = -ee[0].real
    # Return in units of eV and Å.
    # Note: The units of V_ee and V_eh (in q-space) are unknown (we don't know the FT)
    return E_b

def calculate_and_save_binding_energies(materials, nPadding, nFilling):
    N = len(materials)
    E_b_heat_mat = np.zeros((N,N))
    E_b_heat_ylabels = ['n-' + m for m in materials]
    E_b_heat_xlabels = ['p-' + m for m in materials]
    E_b = [[]]*N**2
    bilayer = [[]]*N**2

    count = 0
    for (i_e, e_layer) in enumerate(materials):
        for (i_h, h_layer) in enumerate(materials):
            bilayer[count] = 'n-' + e_layer + ', ' + 'p-' + h_layer
            print(bilayer[count])

            layers = ['BN'] * nPadding + [e_layer] + ['BN'] * nFilling + [h_layer] + ['BN'] * nPadding
            d = [(get_thickness(l) + get_thickness(layers[i+1]))/2 for (i,l) in enumerate(layers[:-1])]

            hs = Heterostructure(structure=layers, d=d, include_dipole=True, wmax=0, qmax=1, d0=0)              

            E_b[count] = get_E_b_for_hs(hs, e_layer, h_layer, nFilling, nPadding)
            E_b_heat_mat[i_e, i_h] = E_b[count]

            count += 1
    
    np.savez('wannier_nFilling=' + str(nFilling) + '_nPadding=' + str(nPadding) + '.npz',
        bilayer=bilayer, E_b=E_b, E_b_heat_mat=E_b_heat_mat,
        E_b_heat_xlabels=E_b_heat_xlabels, E_b_heat_ylabels=E_b_heat_ylabels)

if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    calculate_and_save_binding_energies(materials=['WS2','MoS2','WSe2','MoSe2'], nPadding=0, nFilling=3)
