#np.load('./Materials_iso_wData.npz',COD_id=COD_id,materials=materials_iso[inDatabase],dir_gap=dir_gap_iso[inDatabase],e_avg_vec=e_avg_vec_iso[inDatabase],h_avg_vec=h_avg_vec_iso[inDatabase])
import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
out=np.load('./Materials_iso_stable.npz')
UID_vec=out['uid_vec_iso']

#download json files
#pip install wget
#rm ./jsonfiles/*.json

###FUNCTION
# importing the module
import json
  
# reading the data from the file
def dictionary_convert(link):
    with open(link) as f:
        data = f.read()
    
    print("Data type before reconstruction : ", type(data))
        
    # reconstructing the data as a dictionary
    js = json.loads(data)
    
    print("Data type after reconstruction : ", type(js))
    return js
#READ FILES
#dic =dictionary_convert('./jsonfiles/BN-4a5edc763604.json')
materiale=UID_vec[6]
dic =dictionary_convert('./jsonfiles/'+materiale+'.json')
#BANDSTRUCTURE 
# energies
bs_soc=dic['kwargs']["data"]["bs_soc"]#bandstructure
bandstructurearray=np.array(bs_soc['energies']["__ndarray__"][2])
number_bands=bs_soc['energies']["__ndarray__"][0][0]
kp_bands=bs_soc['energies']["__ndarray__"][0][1]
bs_matrix=bandstructurearray.reshape((number_bands,kp_bands))
#wavenumber
path=bs_soc['path']
kp_path=path['kpts']["__ndarray__"]
points=kp_path[0][0]
coordinates=kp_path[0][1]
coord_path=np.array(kp_path[2])
k_matrix=coord_path.reshape((points,coordinates))
spec_path=path["special_points"]
Gpoint=spec_path['G']["__ndarray__"][2]
Mpoint=spec_path['M']["__ndarray__"][2]
Kpoint=spec_path['K']["__ndarray__"][2]
#spin
spinArray=np.array(bs_soc['sz_mk']["__ndarray__"][2])
spinMatrix=spinArray.reshape((number_bands,kp_bands))
# find the bands close to fermi level
E_fermi=bs_soc['efermi']
for i in range(number_bands):
    bc_vec=bs_matrix[i,:]
    if np.min(bc_vec)>E_fermi:
        bs_val1=bs_matrix[i-2,:]
        bs_val2=bs_matrix[i-1,:]
        bs_cond1=bs_matrix[i,:]
        bs_cond2=bs_matrix[i+1,:]
        spin_val1=spinMatrix[i-2,:]
        spin_val2=spinMatrix[i-1,:]
        spin_cond1=spinMatrix[i,:]
        spin_cond2=spinMatrix[i+1,:]
        break
print(bs_soc['efermi'])
print(np.shape(bs_matrix))
plt.figure(figsize=(9, 5))
plt.plot(range(kp_bands),bs_val1,'k')
plt.plot(range(kp_bands),bs_val2,'k')
plt.plot(range(kp_bands),bs_cond1,'k')
plt.plot(range(kp_bands),bs_cond2,'k')
# for i in range(number_bands):
#     plt.plot(range(kp_bands),bs_matrix[i,:],'k')
plt.plot(range(kp_bands),np.ones((kp_bands))*bs_soc['efermi'],'r--')
plt.title(materiale)
# #plt.xticks(rotation=40,fontsize=12) 
# #plt.ylim([10**(-4),max(max(e_diff_vec),max(h_diff_vec))])
# plt.ylabel(r'thermo stab',fontsize=fS)
# plt.yticks(fontsize=fS)
# plt.tight_layout()
plt.savefig('./plots/'+materiale+'bs.pdf')
# find valence band maximum
print(np.shape(spin_val1))
print(spin_val1[200])
#locate minimum
locMax=np.max(bs_val2)==bs_val2
split_val=spin_val1[locMax]*bs_val1[locMax]+spin_val2[locMax]*bs_val2[locMax]
print(split_val)
print(spin_val1[np.max(bs_val1)==bs_val1])
print(spin_val2[np.max(bs_val2)==bs_val2])
print(np.max(bs_val1))
loc1=k_matrix[locMax]
if np.all(loc1==Gpoint):
    print('located at G')
elif np.all(loc1==Kpoint):
    print('located at K')
elif np.all(loc1==Mpoint):
    print('located at M')

#print(structure['args'])
# for uid in UID_vec:
#     structure ='./jsonfiles/'+uid+'.json'