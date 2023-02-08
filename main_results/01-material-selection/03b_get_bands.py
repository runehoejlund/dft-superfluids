from os import path, chdir
chdir(path.dirname(path.abspath(__file__)))

#np.load('./Materials_iso_wData.npz',COD_id=COD_id,materials=materials_iso[inDatabase],dir_gap=dir_gap_iso[inDatabase],e_avg_vec=e_avg_vec_iso[inDatabase],h_avg_vec=h_avg_vec_iso[inDatabase])
import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
out=np.load('./02_materials_iso_stable.npz')
UID_vec=out['uid_vec_iso']
UID_h=out['uid_vec_hiso']
UID_e=out['uid_vec_eiso']
Material_plot=out['Mat_plot_iso']
material_short_names = np.array([formula.split('-')[-1] for formula in Material_plot])
bandgap_db=out['bandgap_iso']
dir_bandgap_db=['dir_bandgap_iso']

###FUNCTION: convert to dictionary
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
uid_list=UID_vec.tolist()
# uid_list.append('BN-4a5edc763604')

def parse_material(uid):
    short_name = uid.split('-')[0]
    if short_name == 'BN':
        formula = 'BN'
    else:
        Material_plot_idx, = np.where(material_short_names == short_name)
        formula=Material_plot[int(Material_plot_idx)]
    print(formula)
    dic =dictionary_convert('./jsonfiles/'+uid+'.json')
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
    #bandgap
    locMax=np.max(bs_val2)==bs_val2
    if sum(locMax)==2:
            locMax[-1]=0
    eVal=bs_val2[locMax]
    locMin=np.min(bs_cond1)==bs_cond1
    if sum(locMin)==2:
            locMin[-1]=0
    eCond=bs_cond1[locMin]

    cond_min = eCond[0]
    val_max = eVal[0]
    bandgap = cond_min - val_max

    # find valence band maximum
    #locate minimum
    is_h_type = np.any(uid == UID_h)
    is_e_type = np.any(uid == UID_e)
    val_split1, val_split2, loc_val, cond_split1, cond_split2, loc_cond = None, None, None, None, None, None
    if is_h_type:
        locMax=np.max(bs_val2)==bs_val2
        if sum(locMax)==2:
            locMax[-1]=0
        split_val=spin_val1[locMax]*bs_val1[locMax]+spin_val2[locMax]*bs_val2[locMax]
        split2_val=bs_val2[locMax]-bs_val1[locMax]
        val_split1 = split_val[0]
        val_split2 = split2_val[0]
        print(split_val)
        print(spin_val1[np.max(bs_val1)==bs_val1])
        print(spin_val2[np.max(bs_val2)==bs_val2])
        print(np.max(bs_val1))
        loc1=k_matrix[locMax]
        if np.all(loc1==Gpoint):
            print('located at G')
            loc_val = 'G'
        elif np.all(loc1==Kpoint):
            print('located at K')
            loc_val = 'K'
        elif np.all(loc1==Mpoint):
            print('located at M')
            loc_val = 'M'
        else:
            if np.arange(400)[locMax][0]==229:
                loc_val = 'K'
    if is_e_type:
        locMin=np.min(bs_cond1)==bs_cond1
        if sum(locMin)==2:
            locMin[-1]=0
        split_cond=spin_cond1[locMin]*bs_cond1[locMin]+spin_cond2[locMin]*bs_cond2[locMin]
        split2_cond=bs_cond2[locMin]-bs_cond1[locMin]
        cond_split1 = split_cond[0]
        cond_split2 = split2_cond[0]
        print(formula)
        print(split_cond)
        print(split2_cond)
        print(spin_cond1[locMin])
        print(spin_cond2[locMin])
        loc1=k_matrix[locMin]
        if np.all(loc1==Gpoint):
            print('located at G')
            loc_cond = 'G'
        elif np.all(loc1==Kpoint):
            print('located at K')
            loc_cond = 'K'
        elif np.all(loc1==Mpoint):
            print('located at M')
            loc_cond = 'M'
        else:
            if np.arange(400)[locMin][0]==229:
                loc_cond = 'K'

    return (formula, cond_min, val_max, bandgap, is_h_type, is_e_type, val_split1, val_split2, loc_val, cond_split1, cond_split2, loc_cond,
        bs_val1, bs_val2, bs_cond1, bs_cond2, locMin, locMax, kp_bands, bs_soc)

bandgap_vec=[]
uid_cond=[]
uid_val=[]
formula_cond=[]
formula_val=[]
split_val_vec=[]
split_cond_vec=[]
split2_val_vec=[]
split2_cond_vec=[]
loc_val_vec=[]
loc_cond_vec=[]

cond_min_vec = []
val_max_vec = []
#READ FILES

_, BN_cond_min, BN_val_max, *_ = parse_material('BN-4a5edc763604')

for uid in uid_list:
    formula, cond_min, val_max, bandgap, is_h_type, is_e_type, val_split1, val_split2, loc_val, cond_split1, cond_split2, loc_cond, bs_val1, bs_val2, bs_cond1, bs_cond2, locMin, locMax, kp_bands, bs_soc = parse_material(uid)  

    cond_min_vec.append(cond_min)
    val_max_vec.append(val_max)
    bandgap_vec.append(bandgap)
    if is_h_type:
        split_val_vec.append(val_split1)
        split2_val_vec.append(val_split2)
        uid_val.append(uid)
        formula_val.append(formula)
        loc_val_vec.append(loc_val)
    if is_e_type:
        split_cond_vec.append(cond_split1)
        split2_cond_vec.append(cond_split2)
        uid_cond.append(uid)
        formula_cond.append(formula)
        loc_cond_vec.append(loc_cond)  

    # #PLOT
    # plt.figure(figsize=(9, 5))
    # xaxis=np.arange(kp_bands)
    # Legend=['G-line','M-line','K-line']
    # #special points
    # step=(max(bs_cond2)-min(bs_val1))/10
    # vertical_line=np.arange(min(bs_val1),max(bs_cond2)+step-0.001,step)
    # plt.plot(np.ones((11))*xaxis[0],vertical_line,'k--')
    # plt.plot(np.ones((11))*xaxis[145],vertical_line,'k--')
    # plt.plot(np.ones((11))*xaxis[229],vertical_line,'k--')
    # #extrama
    # if is_e_type:
    #     plt.plot(np.ones((2))*xaxis[locMin],[bs_cond1[locMin],bs_cond2[locMin]],'b-o')
    #     #Legend.append('point='+loc_cond_vec[-1]+'_split={:.2f} meV_split2={:.2f} meV'.format(split_cond_vec[-1]*10**3,split2_cond_vec[-1]*10**3))
    #     Legend.append('point='+loc_cond_vec[-1]+'_split2={:.2f} meV'.format(split2_cond_vec[-1]*10**3))
    # if is_h_type:
    #     plt.plot(np.ones((2))*xaxis[locMax],[bs_val1[locMax],bs_val2[locMax]],'m-o')
    #     #Legend.append('point='+loc_val_vec[-1]+'_split={:.2f} meV_split2={:.2f} meV'.format(split_val_vec[-1]*10**3,split2_val_vec[-1]*10**3))
    #     Legend.append('point='+loc_val_vec[-1]+'_split2={:.2f} meV'.format(split2_val_vec[-1]*10**3)) 
    # plt.plot(xaxis[locMin],bs_cond1[locMin], 'yx', label='cond min')
    # plt.plot(xaxis[locMax],bs_val2[locMax], 'yx', label='cond max')
    # plt.legend(Legend)
    # #bands
    # plt.plot(xaxis,bs_val1,'k')
    # plt.plot(xaxis,bs_val2,'r')
    # plt.plot(xaxis,bs_cond1,'k')
    # plt.plot(xaxis,bs_cond2,'r')
    # # for i in range(number_bands):
    # #     plt.plot(range(kp_bands),bs_matrix[i,:],'k')
    # plt.plot(xaxis,np.ones((kp_bands))*bs_soc['efermi'],'g--')
    # plt.title(uid)
    # plt.ylabel('E [eV]')
    # # #plt.xticks(rotation=40,fontsize=12) 
    # # #plt.ylim([10**(-4),max(max(e_diff_vec),max(h_diff_vec))])
    # # plt.ylabel(r'thermo stab',fontsize=fS)
    # # plt.yticks(fontsize=fS)
    # # plt.tight_layout()
    # plt.savefig('./plots/'+uid+'_bs.png')


plt.figure(figsize=(12,8))
plt.title('band alignments')
plt.hlines(BN_cond_min, xmin=0, xmax=len(Material_plot), colors=['red'])
plt.hlines(BN_val_max, xmin=0, xmax=len(Material_plot), colors=['red'])
plt.xticks(rotation=40,fontsize=12) 
plt.plot(Material_plot, cond_min_vec, 'b-o', label='cond. min.')
plt.plot(Material_plot, val_max_vec, 'b--o', label='val. max.')

plt.plot(Material_plot[np.array(val_max_vec) < BN_val_max], np.array(val_max_vec)[np.array(val_max_vec) < BN_val_max], 'r*')
plt.plot(Material_plot[np.array(val_max_vec) < BN_val_max], np.array(cond_min_vec)[np.array(val_max_vec) < BN_val_max], 'r*')
plt.plot(Material_plot[np.array(cond_min_vec) > BN_cond_min], np.array(val_max_vec)[np.array(cond_min_vec) > BN_cond_min], 'r*')
plt.plot(Material_plot[np.array(cond_min_vec) > BN_cond_min], np.array(cond_min_vec)[np.array(cond_min_vec) > BN_cond_min], 'r*')

plt.legend()
plt.savefig('./plots/band_alignments.png')

print(formula_cond[5:11])
print(np.round(split_cond_vec,3)[5:11])
print(np.round(split2_cond_vec,3)[5:11])
print(loc_cond_vec)
print(formula_val[5:15])
print(np.round(split_val_vec,3)[5:15])
print(np.round(split2_val_vec,3)[5:15])
print(loc_val_vec)
print(Material_plot)
print(np.round(bandgap_vec,2))
print(len(uid_val),len(uid_cond),len(split_val_vec),len(split_cond_vec),len(loc_val_vec),len(loc_cond_vec))
    #print(structure['args'])
    # for uid in UID_vec:
    #     structure ='./jsonfiles/'+uid+'.json'

np.savez('./03_so_split_extremum-loc.npz',UID_vec=UID_vec,Material_plot=Material_plot,bandgap_vec=bandgap_vec, formula_cond=formula_cond,uid_cond=uid_cond,split_cond_vec=split_cond_vec,split2_cond_vec=split2_cond_vec,loc_cond_vec=loc_cond_vec,formula_val=formula_val,uid_val=uid_val,split_val_vec=split_val_vec,split2_val_vec=split2_val_vec,loc_val_vec=loc_val_vec,bandgap_db=bandgap_db,dir_bandgap_db=dir_bandgap_db)