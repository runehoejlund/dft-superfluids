out = np.load('./materials_iso_stable.npz')
h_iso = out['h_iso'].flatten()
e_iso = out['e_iso'].flatten()
m_e_all = out['e_avg_vec']
m_h_all = out['h_avg_vec']
m_e = m_e_all[e_iso]
m_h = m_h_all[h_iso]