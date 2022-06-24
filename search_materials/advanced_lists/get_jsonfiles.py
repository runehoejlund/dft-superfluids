#np.load('./Materials_iso_wData.npz',COD_id=COD_id,materials=materials_iso[inDatabase],dir_gap=dir_gap_iso[inDatabase],e_avg_vec=e_avg_vec_iso[inDatabase],h_avg_vec=h_avg_vec_iso[inDatabase])
import numpy as np
import matplotlib.pyplot as plt
import ase.db
out=np.load('./Materials_iso_stable.npz')
UID_vec=out['uid_vec_iso']

print(UID_vec)

#download json files
#pip install wget
import wget
#rm ./jsonfiles/*.json
#https://cmrdb.fysik.dtu.dk/c2db/row/As4Ca4-bf7bbbdbefe0/data/results-asr.bandstructure.json
link ='https://cmrdb.fysik.dtu.dk/c2db/row/'+'BN-4a5edc763604'+'/data/results-asr.bandstructure.json/json'
file_name = wget.download(link,out='./jsonfiles/BN-4a5edc763604.json')
for uid in UID_vec:
    link ='https://cmrdb.fysik.dtu.dk/c2db/row/'+uid+'/data/results-asr.bandstructure.json/json'
    file_name = wget.download(link,out='./jsonfiles/'+uid+'.json')

print(file_name)
