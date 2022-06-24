import numpy as np
import matplotlib.pyplot as plt
#
out=np.load('./Materials_c2db.npz')

bandgap=out['bandgap']
dir_bandgap=out['dir_bandgap']
materials=out['material_c2db_list']
emass1_vec=out['emass1_vec']
emass2_vec=out['emass2_vec']
hmass1_vec=out['hmass1_vec']
hmass2_vec=out['hmass2_vec']

#average masses
e_avg_vec=(emass1_vec+emass2_vec)/2
h_avg_vec=(hmass1_vec+hmass2_vec)/2
cut=0.05
e_diff_vec=abs(emass1_vec-emass2_vec)/e_avg_vec
h_diff_vec=abs(hmass1_vec-hmass2_vec)/h_avg_vec
e_iso=[e_diff_vec<cut]
h_iso=[h_diff_vec<cut]
iso=[e_iso[i]*h_iso[i] for i in range(len(e_iso))]
print(iso)
print(emass1_vec,emass2_vec,e_diff_vec)
materials_isotropic=materials[iso]
print(materials_isotropic)
print(materials[h_iso])
plt.figure(figsize=(9, 3))
plt.semilogy(materials,e_diff_vec,'b-o')
plt.semilogy(materials,0.05*np.ones((len(e_diff_vec))))
#plt.ylabel('some numbers')
plt.xticks(rotation=90) 
plt.savefig('./sorting.pdf')
print(len(e_diff_vec))
print(len(materials_isotropic))
print(materials[h_iso])
print(len(materials[h_iso]))

np.savez('./Materials_iso.npz',materials=materials,h_iso=h_iso,e_iso=e_iso,e_avg_vec=e_avg_vec,h_avg_vec=h_avg_vec,bandgap=bandgap,dir_bandgap=dir_bandgap)