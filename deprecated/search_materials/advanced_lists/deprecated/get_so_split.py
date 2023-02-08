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
dic =dictionary_convert('./jsonfiles/BN-4a5edc763604.json')
bs_soc=dic['kwargs']["data"]["bs_soc"]
bandstructurearray=np.array(bs_soc['energies']["__ndarray__"][2])
number_bands=bs_soc['energies']["__ndarray__"][0][0]
kp_bands=bs_soc['energies']["__ndarray__"][0][1]
bs_matrix=bandstructurearray.reshape((number_bands,kp_bands))
print(bs_soc['efermi'])
print(np.shape(bs_matrix))
plt.figure(figsize=(9, 5))
for i in range(number_bands):
    plt.plot(range(kp_bands),bs_matrix[i,:],'k-o')
# #plt.xticks(rotation=40,fontsize=12) 
# #plt.ylim([10**(-4),max(max(e_diff_vec),max(h_diff_vec))])
# plt.ylabel(r'thermo stab',fontsize=fS)
# plt.yticks(fontsize=fS)
# plt.tight_layout()
plt.savefig('./plots/bs.pdf')
# plt.close()
#print(structure['args'])
# for uid in UID_vec:
#     structure ='./jsonfiles/'+uid+'.json'