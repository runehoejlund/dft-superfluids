import numpy as np
import matplotlib.pyplot as plt
#nice plotting
from matplotlib import rcParams
rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern Roman"],
    "font.size": 8})
rcParams['axes.titlepad'] = 20
#
out=np.load('./Materials_crystal_c2db.npz')
Material_plot=out['Material_plot']
bandgap=out['bandgap']
dir_bandgap=out['dir_bandgap']
materials=out['material_c2db_list']
emass1_vec=out['emass1_vec']
emass2_vec=out['emass2_vec']
hmass1_vec=out['hmass1_vec']
hmass2_vec=out['hmass2_vec']
print([hmass1_vec,hmass2_vec])
#print(materials)
#average masses
e_avg_vec=(emass1_vec+emass2_vec)/2
h_avg_vec=abs(hmass1_vec+hmass2_vec)/2
cut=0.02
e_diff_vec=abs(emass1_vec-emass2_vec)/e_avg_vec
h_diff_vec=abs(hmass1_vec-hmass2_vec)/h_avg_vec
print(h_diff_vec)
e_iso=e_diff_vec<cut
h_iso=h_diff_vec<cut
print(h_iso)
print(len(Material_plot))
print(len(materials))
#print(np.shape(h_iso))
#print(np.shape(materials))
#print(iso)
#print(emass1_vec,emass2_vec,e_diff_vec)
materials_e_iso=materials[e_iso]
materials_h_iso=materials[h_iso]
#print(materials_isotropic)
#print(materials_e_iso)
#print(materials_h_iso)
plt.figure(figsize=(9, 5))
plt.semilogy(Material_plot,e_diff_vec,'b-o')
plt.semilogy(Material_plot,h_diff_vec,'r-o')
N=len(Material_plot)
plt.semilogy(Material_plot,cut*np.ones((len(e_diff_vec))),'k-')
#plt.ylabel('some numbers')
plt.legend(['e-mass','h-mass','cut'])
plt.semilogy(Material_plot[~e_iso],e_diff_vec[~e_iso],'w*')
plt.semilogy(Material_plot[~h_iso],h_diff_vec[~h_iso],'w*')
plt.xticks(rotation=40) 
plt.ylim([10**(-4),max(max(e_diff_vec),max(h_diff_vec))])
plt.ylabel(r'$|\mathrm{diff}|/\mathrm{avg}$',Fontsize=12)
plt.tight_layout()
plt.savefig('./sorting.pdf')
#print(len(e_diff_vec))
#print(len(materials_isotropic))
print(len(materials_e_iso))
print(len(materials_h_iso))
#print(e_avg_vec[materials=='formula=GeO2,crystal_type=AB2-187-bi'])
#print(e_avg_vec[materials=='formula=GeO2,crystal_type=AB2-164-bd'])
#print(e_avg_vec)
#print(materials)
print(materials_e_iso)
print(materials_h_iso)
print('N-DOPED: number:', len(Material_plot[e_iso]),', materials', Material_plot[e_iso])
print('P-DOPED: number:', len(Material_plot[h_iso]),', materials',Material_plot[h_iso])
iso=np.array([e_iso[i]*h_iso[i] for i in range(N)])
iso_flat=iso.flatten()
print('ELEMENTS IN COMMON: number',len(Material_plot[iso_flat]),', materials', Material_plot[iso_flat])
uNION=np.unique(np.hstack((Material_plot[h_iso],Material_plot[e_iso])))
print('UNION: number', len(uNION),', materials',uNION)
np.savez('./Materials_iso_crystal.npz',Material_plot=Material_plot,materials=materials,materials_e_iso=materials_e_iso,materials_h_iso=materials_h_iso,h_iso=h_iso,e_iso=e_iso,e_avg_vec=e_avg_vec,h_avg_vec=h_avg_vec,bandgap=bandgap,dir_bandgap=dir_bandgap)