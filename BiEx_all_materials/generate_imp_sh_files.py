from os import path, chdir
chdir(path.dirname(path.abspath(__file__)))

import numpy as np

#define function that writes values imp and sh files
def printBiExinp(filename,material,me,mh,so_split_e,so_split_h,loc_e,loc_h,d,QEH,hours=24,cores='40'):
    
    #file name to write
    #QEH
    if QEH==True:
        logic='T'
        description='_QEH'    
    if QEH==False:
        logic='T' # Set to 'T' to read interaction from .dat file
        description='_analytic'
    fullname='./out/' + material+description+'_MF.inp'
    #write
    fileout=open(fullname, 'w')
    filein=open('inptemplate.inp','r')
    string=filein.read()

    #some other input parameters
    # from our analysis of the materials we have seen that at the Gamma point there is no so-splitting
    # while at the K point there is always a finite splitting
    if max(so_split_e,so_split_h)>0:
        norb=2
        gspin=1
    else:
        norb=1
        gspin=2
    #the parameter gvalley should be developed according to Fredrik, so we have one for
    #the n-doped and p-doped material - see word-document for more info
    gvalley=2
    if loc_e=='G':
        gvalley_e=1
    elif loc_e=='K':
        gvalley_e=2
    if loc_h=='G':
        gvalley_h=1
    elif loc_h=='K':
        gvalley_h=2

    
    #dictionary for inp-file
    inpParam={ 'filename':material+description+'_MF',
                'structure': material + description,
                'job':'MF',
                'dstep':0.00010,
                'plotPoints': 90,
                'cores': cores,
                'logical': logic,
                'me': me,
                'mh': mh,
                'soc_split_e': so_split_e,
                'soc_split_h': so_split_h,
                'distance': d,
                'norb': norb,
                'gspin':gspin,
                'gvalley':gvalley}
    #print(string)
    print(string%inpParam,file=fileout)

    fileout.close()
    filein.close()

    #writing sh-file
    #partion is determined number of cores
    partition = 'xeon'+cores

    fileout=open('./out/' + material+description+'_MF.sh','w')
    filein=open('shtemplate.sh','r')
    string=filein.read()
    shParams={'out': './slurm_out/' + material + description+'_MF_%j_out.txt',
            'err': './slurm_out/' + material + description+'_MF_%jerr.txt',
            'setup': '',
            'inp': material+description+'_MF.inp',
            'hours': hours,
            'cores': cores,
            'partition': partition}
    print(string%shParams,file=fileout)
    fileout.close()
    filein.close()

#run through
def run_through_materials(loc_cond_vec,loc_val_vec,split_cond,split_val,materials_e,materials_h,e_avg_vec_iso,h_avg_vec_iso,Mat_plot_iso,d_List,nPadding, nFilling):
    N_e = len(materials_e)
    N_h = len(materials_h)
    count=0
    for (i_e, e_layer) in enumerate(materials_e):
        for (i_h, h_layer) in enumerate(materials_h):
            if loc_cond_vec[i_e] != loc_val_vec[i_h]:
                print(loc_cond_vec[i_e] + ' != ' + loc_val_vec[i_h] + ' is an indirect bandgap. Skipping.')
                continue
            material = 'n-' + e_layer + '_' + 'p-' + h_layer
            filename=material
            print('{} out of {}'.format(count+1,N_e*N_h))
            print(material)
            count+=1
            #extract parameters that we will use to solve the gap-equation
            me=e_avg_vec_iso[i_e]
            mh=h_avg_vec_iso[i_h]
            so_split_e=split_cond[i_e]
            so_split_h=split_val[i_h]
            loc_e=loc_cond_vec[i_e]
            loc_h=loc_val_vec[i_h]
            d=d_List[e_layer==Mat_plot_iso][0]/2+d_List[h_layer==Mat_plot_iso][0]/2+3.33
            print(d,loc_e,loc_h,so_split_e,so_split_h)
            #print to files
            #using QEH-potential
            printBiExinp(filename,material,me,mh,so_split_e,so_split_h,loc_e,loc_h,d,QEH=True,hours=24,cores='40')
            #using analytical-potential
            printBiExinp(filename,material,me,mh,so_split_e,so_split_h,loc_e,loc_h,d,QEH=False,hours=24,cores='40')

if __name__ == '__main__':
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    #out=np.load()
    #materials=out['materials']
    import numpy as np
    #load materials
    out=np.load('./Materials_iso_stable.npz')
    materials=out['materials']
    h_iso=out['h_iso'].flatten()
    e_iso=out['e_iso'].flatten()
    Material_plot=out['Material_plot']
    materials_e=Material_plot[e_iso]
    materials_h=Material_plot[h_iso]
    e_avg_vec=out['e_avg_vec']
    h_avg_vec=out['h_avg_vec']
    e_avg_vec_iso=e_avg_vec[e_iso]
    h_avg_vec_iso=e_avg_vec[h_iso]
    Mat_plot_iso=out['Mat_plot_iso']
    d_List=out['d_List']
    out2=np.load('./so_split_extremum-loc.npz')
    split_cond=out2['split2_cond_vec']
    split_val=out2['split2_val_vec']
    loc_cond_vec=out2['loc_cond_vec']
    loc_val_vec=out2['loc_val_vec']

    #choose materials
    iNDEX1=0
    iNDEX2e=-1
    iNDEX2h=-1
    #iNDEX2e=len(e_avg_vec_iso)
    #iNDEX2h=len(h_avg_vec_iso)
    run_through_materials(loc_cond_vec=loc_cond_vec[iNDEX1:iNDEX2e],loc_val_vec=loc_val_vec[iNDEX1:iNDEX2h],split_cond=split_cond[iNDEX1:iNDEX2e],split_val=split_val[iNDEX1:iNDEX2h],materials_e=materials_e[iNDEX1:iNDEX2e],materials_h=materials_h[iNDEX1:iNDEX2h],e_avg_vec_iso=e_avg_vec_iso[iNDEX1:iNDEX2e],h_avg_vec_iso=h_avg_vec_iso[iNDEX1:iNDEX2h], Mat_plot_iso=Mat_plot_iso,d_List=d_List,nPadding=0, nFilling=1)