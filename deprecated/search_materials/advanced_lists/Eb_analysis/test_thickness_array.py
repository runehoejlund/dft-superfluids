#load materials
import numpy as np
out=np.load('../Materials_iso_stable.npz')
materials=out['materials']
h_iso=out['h_iso'].flatten()
e_iso=out['e_iso'].flatten()
Material_plot=out['Material_plot']
Mat_plot_iso=out['Mat_plot_iso']
uid_vec_iso=out['uid_vec_iso']
materials_e=Material_plot[e_iso]
materials_h=Material_plot[h_iso]
e_avg_vec=out['e_avg_vec']
h_avg_vec=out['h_avg_vec']
e_avg_vec_iso=e_avg_vec[e_iso]
h_avg_vec_iso=e_avg_vec[h_iso]
d_List=out['d_List']
print(materials_e)
print(Material_plot)
print(uid_vec_iso)
#get thickness by
print(d_List['H-CrS2'==Mat_plot_iso][0])