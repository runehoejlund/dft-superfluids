#np.load('./Materials_iso_wData.npz',COD_id=COD_id,materials=materials_iso[inDatabase],dir_gap=dir_gap_iso[inDatabase],e_avg_vec=e_avg_vec_iso[inDatabase],h_avg_vec=h_avg_vec_iso[inDatabase])
import numpy as np
import matplotlib.pyplot as plt
import ase.db
out=np.load('./Materials_iso_wData.npz')
COD_id=out['COD_id']
dir_gap=out['dir_gap']
e_iso=out['e_iso']
materials=out['materials']
#inspect
print(COD_id)
print(materials)
print(dir_gap)
print(e_iso)
print(materials[e_iso])
print(materials[dir_gap])
#download json files
#pip install wget
import wget
link = 'https://cmrdb.fysik.dtu.dk/lowdim/row/9007661/data/structure.json'
link ='https://cmrdb.fysik.dtu.dk/c2db/row/BN-4a5edc763604/data/structure.json'
file_name = wget.download(link)
print(file_name)
#for 
#    link = 'http://www.randomdatabase.com/database_files/csv/main_database.csv'
#    file_name = wget.download(site_url)