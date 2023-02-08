out = np.load('./materials_iso_stable.npz')
h_iso = out['h_iso'].flatten()
e_iso = out['e_iso'].flatten()
e_avg_vec = out['e_avg_vec']
h_avg_vec = out['h_avg_vec']
m_e = e_avg_vec[e_iso]
m_h = e_avg_vec[h_iso]