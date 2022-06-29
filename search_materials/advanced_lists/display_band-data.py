#display band-data
#import
import numpy as np
import matplotlib.pyplot as plt
#
out=np.load('./so_split_extremum-loc.npz')
Material_plot=out['Material_plot']
bandgap_vec=out['bandgap_vec']
bandgap_db=out['bandgap_db']
#plot bandgaps
plt.figure(figsize=(9, 5))
plt.plot(Material_plot,bandgap_vec,'k-o')
plt.plot(Material_plot,bandgap_db,'m*')
plt.xticks(rotation=40,fontsize=12)
plt.ylabel('Bandgag [eV]')
plt.legend(['found with so from jsonfiles','obtained from c2db'])
plt.tight_layout()
plt.savefig('./plots/bandgap_so.png')

#
split_cond=out['split2_cond_vec']
split_val=out['split2_val_vec']
loc_cond_vec=out['loc_cond_vec']
loc_val_vec=out['loc_val_vec']
uid_val=out['uid_val']
uid_cond=out['uid_cond']
formula_val=out['formula_val']
formula_cond=out['formula_cond']
#valence band splitting
plt.figure(figsize=(9, 5))
plt.plot(formula_val,split_val,'k-o')
plt.plot(formula_val['G'==loc_val_vec],split_val['G'==loc_val_vec],'b*')
plt.plot(formula_val['K'==loc_val_vec],split_val['K'==loc_val_vec],'r*')
plt.legend(['all','at G','at K'])
plt.xticks(rotation=40,fontsize=12)
plt.ylabel('split val [eV]')
plt.tight_layout()
#plt.savefig('./plots/split_val_so.png')
#conduction band splitting
plt.figure(figsize=(9, 5))
plt.plot(formula_cond,split_cond,'k-o')
plt.plot(formula_cond['G'==loc_cond_vec],split_cond['G'==loc_cond_vec],'b*')
plt.plot(formula_cond['K'==loc_cond_vec],split_cond['K'==loc_cond_vec],'r*')
plt.legend(['all','at G','at K'])
plt.xticks(rotation=40,fontsize=12)
plt.ylabel('split cond [eV]')
plt.tight_layout()
#plt.savefig('./plots/split_cond_so.png')
print(Material_plot)
print(len(Material_plot))
print(len(split_cond))