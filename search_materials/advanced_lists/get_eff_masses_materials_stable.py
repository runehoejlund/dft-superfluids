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
#load
out=np.load('./Materials_stable.npz')
Material_plot=out['Material_plot']
bandgap=out['bandgap']
dir_bandgap=out['dir_bandgap']
materials=out['material_c2db_list']
emass1_vec=out['emass1_vec']
emass2_vec=out['emass2_vec']
hmass1_vec=out['hmass1_vec']
hmass2_vec=out['hmass2_vec']
ehull_vec=out['ehull_vec']
uid_vec=out['uid_vec']
thermo_stab=out['thermo_stab']
#average masses and isotropy
e_avg_vec=(emass1_vec+emass2_vec)/2
h_avg_vec=abs(hmass1_vec+hmass2_vec)/2
cut=0.02
e_diff_vec=abs(emass1_vec-emass2_vec)/e_avg_vec
h_diff_vec=abs(hmass1_vec-hmass2_vec)/h_avg_vec
e_iso=e_diff_vec<cut
h_iso=h_diff_vec<cut
N_iso=len(h_iso)
iso=np.repeat(False,N_iso)
for i in range(N_iso):
    if h_iso[i]==1:
        iso[i]=True
    elif e_iso[i]==1:
        iso[i]=True
    else:
        iso[i]=False
materials_e_iso=materials[e_iso]
materials_h_iso=materials[h_iso]
materials_iso=materials[iso]
#plot
#isotropy selection
fS=16
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
plt.yticks(fontsize=16)
plt.ylabel(r'$|\mathrm{diff}|/\mathrm{avg}$',fontsize=fS)
plt.tight_layout()
plt.savefig('./plots/sorting.pdf')
plt.close()
#plot bandgaps
plt.figure(figsize=(9, 5))
plt.plot(Material_plot[iso],bandgap[iso],'k-o')
plt.xticks(rotation=40,fontsize=12) 
#plt.ylim([10**(-4),max(max(e_diff_vec),max(h_diff_vec))])
plt.ylabel(r'Bandgap [eV]',fontsize=fS)
plt.yticks(fontsize=fS)
plt.tight_layout()
plt.savefig('./plots/bandgap.pdf')
plt.close()
#plot thermostab
plt.figure(figsize=(9, 5))
plt.plot(Material_plot[iso],thermo_stab[iso],'k-o')
plt.xticks(rotation=40,fontsize=12) 
#plt.ylim([10**(-4),max(max(e_diff_vec),max(h_diff_vec))])
plt.ylabel(r'thermo stab',fontsize=fS)
plt.yticks(fontsize=fS)
plt.tight_layout()
plt.savefig('./plots/thermo_stab.pdf')
plt.close()
#convew hull
plt.figure(figsize=(9, 5))
plt.plot(Material_plot[iso],ehull_vec[iso],'k-o')
plt.xticks(rotation=40,fontsize=12) 
#plt.ylim([10**(-4),max(max(e_diff_vec),max(h_diff_vec))])
plt.ylabel(r'Energy over convex hull [eV]',fontsize=fS)
plt.yticks(fontsize=fS)
plt.tight_layout()
plt.savefig('./plots/ehull.pdf')
plt.close()
#print materials
print('N-DOPED: number:', len(Material_plot[e_iso]),', materials', Material_plot[e_iso])
print('P-DOPED: number:', len(Material_plot[h_iso]),', materials',Material_plot[h_iso])
eh_iso=np.array([e_iso[i]*h_iso[i] for i in range(N)])
iso_flat=eh_iso.flatten()
print('ELEMENTS IN COMMON: number',len(Material_plot[iso_flat]),', materials', Material_plot[iso_flat])
#uNION=np.unique(np.hstack((Material_plot[h_iso],Material_plot[e_iso])))
print('UNION: number', sum(iso),', materials',Material_plot[iso])
#write txt files
print(len(uid_vec))
print(uid_vec)
uid_vec_iso=uid_vec[iso]
uid_vec_eiso=uid_vec[e_iso]
uid_vec_hiso=uid_vec[h_iso]
#np.savetxt('uid_for_which_we_need_a_thickness.txt', uid_vec)
uid_list=uid_vec_iso.tolist()
with open('uid_for_which_we_need_a_thickness.txt', "w") as output:
    #output.write(str(uid_list))
    for item in uid_list:
        # write each item on a new line
        output.write("%s\n" % item)
    print('Done')
#load thicknesses from Sahar
d_List=[]
#load uid's that we would like a thickness for
with open('thicknesses_Sahar.txt', 'r') as content:
    for line in content:
        #x=line[:-1]
        currentline = line.split(",")
        uid=currentline[0]
        thickness=currentline[2]
        thick_number=thickness.split(": ")
        d=thick_number[1][:-1]
        d_List.append(float(d))
        #print(uid)
        #print(currentline[2][:-1])
        #print(d)
#
plt.figure(figsize=(9, 5))
plt.plot(Material_plot[iso],d_List,'k-o')
plt.xticks(rotation=40,fontsize=12) 
#plt.ylim([10**(-4),max(max(e_diff_vec),max(h_diff_vec))])
plt.ylabel(r'thickness [Å]',fontsize=fS)
plt.yticks(fontsize=fS)
plt.tight_layout()
plt.savefig('./plots/thicknesses.png')
plt.close()

bandgap_iso=bandgap[iso]
dir_bandgap_iso=dir_bandgap[iso]
np.savez('./Materials_iso_stable.npz',uid_vec_eiso=uid_vec_eiso,uid_vec_hiso=uid_vec_hiso,uid_vec_iso=uid_vec_iso,Mat_plot_iso=Material_plot[iso],Material_plot=Material_plot,materials=materials,materials_e_iso=materials_e_iso,materials_h_iso=materials_h_iso,h_iso=h_iso,e_iso=e_iso,e_avg_vec=e_avg_vec,h_avg_vec=h_avg_vec,bandgap_iso=bandgap_iso,dir_bandgap_iso=dir_bandgap_iso,d_List=d_List)