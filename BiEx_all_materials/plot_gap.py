
# %%
from os import path, chdir
chdir(path.dirname(path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import matplotlib as mpl

from matplotlib.colors import ListedColormap, LinearSegmentedColormap

def get_cmap(cmap, min_p=0.3, N_cmap=256):
    cmap = plt.get_cmap(cmap)
    N_cmap = 256
    return ListedColormap(cmap(np.linspace(0,1,int(N_cmap/(1-min_p))))[-N_cmap:,:])

from matplotlib import rcParams
rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern Roman"],
    "font.size": 16})
rcParams['axes.titlepad'] = 20

def load_Deltak(filename):
    could_open = True
    try:
        with open(filename) as f:
            lines = f.readlines()
    except:
        print('could not open: '+filename)
        could_open = False
        return 0
    densloc = []
    deltamax = []
    found_cutoff_dens = False
    cutoffdens = 0
    cfrac = []
    if could_open:
        for linenumber, line in enumerate(lines):
            if linenumber == 2:
                if "Delta(2)" in line.split(','):
                    cindex = 9
                else:
                    cindex = 8
                continue
            elif line[0] == '#':
                continue
            l1 = line.split()
            if not found_cutoff_dens:
                cutoffdens = float(l1[0])
            densloc.append(float(l1[0]))
            if float(l1[cindex]) < 0.2:
                found_cutoff_dens = True
            deltamax.append(float(l1[3]))
            tmp = float(l1[cindex])
            cfrac.append(tmp)
        if not found_cutoff_dens:
            print('WARNING, NO CUTOFF DENS'+filename)
    return cutoffdens, densloc, deltamax, cfrac


def make_figure(figname, xmax, N, postfix=''):
    vdWH = np.load('vdWH' + '_nFilling=1_nPadding=0.npz')
    vdWH_E_b = vdWH['E_b']
    vdWH_bilayers = list(vdWH['bilayers'])
    # vdWH_bilayers = ["_".join(b.split(", ")) for b in vdWH['bilayers']]
    vmin = np.min(vdWH_E_b)*10**3
    vmax = np.max(vdWH_E_b)*10**3
    def get_color(bilayer_E_b, vmin, vmax, min_p = 0.3):
        cmap = plt.get_cmap('Blues') 
        p = min_p + (1-min_p)*(bilayer_E_b*10**3 - vmin)/(vmax - vmin)
        return cmap(p)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = get_cmap('Blues')
    
    ppi = 150
    figw = 500
    figh = 450
    SMALL_SIZE = 10
    MEDIUM_SIZE = 12
    plt.rc('font', size=SMALL_SIZE)
    plt.rc('axes', titlesize=SMALL_SIZE)
    plt.rc('axes', labelsize=MEDIUM_SIZE)
    plt.rc('xtick', labelsize=MEDIUM_SIZE)
    plt.rc('ytick', labelsize=MEDIUM_SIZE)
    plt.rc('legend', fontsize=SMALL_SIZE)
    # plt.gcf().subplots_adjust(bottom=0.15)

    dens = []
    densarray = []
    delta = []
    condfrac = []

    filenames = Path('out' + postfix).glob('n-*'+figname+'_MF/DeltaN_MF_iTemp001')
    names = []
    bilayers = []
    E_b = []
    for i, filename in enumerate(filenames):
        fn = str(filename)
        # if 'n-H-WSe2_p-H-MoSe2' not in fn:
        #     continue
        cutoffdens, densloc, deltamax, cfrac = load_Deltak(fn)
        name = fn.split('/')[1]
        bilayer = ', '.join(name.split('_')[:-2])
        try:
            E_b.append(vdWH_E_b[vdWH_bilayers.index(bilayer)])
        except:
            print(bilayer + ' is not in bilayers')
        bilayers.append(bilayer)
        names.append(name)
        dens.append(cutoffdens)
        densarray.append(densloc)
        delta.append(deltamax)
        condfrac.append(cfrac)

    # plot_index = sorted(range(len(dens)), key=lambda sub: dens[sub])[-N:]

    cutoff_argsort = np.argsort(np.array(dens))[::-1]
    dens = np.array(dens)[cutoff_argsort]
    densarray = np.array(densarray)[cutoff_argsort,:]
    delta = np.array(delta)[cutoff_argsort,:]
    condfrac = np.array(condfrac)[cutoff_argsort,:]
    ones = np.ones(densarray.shape[1])
    names_sorted = list(np.array(names)[cutoff_argsort])

    fig = plt.figure(figsize=((figw + 380) / ppi, figh / ppi),
                     dpi=ppi, constrained_layout=True)
    # fig = plt.figure(figsize=((figw + 380) / ppi, figh / ppi),
    #                  dpi=ppi)
    ax = fig.add_subplot(1, 1, 1)
    # fig2 = plt.figure(figsize=(figw / ppi, figh / ppi),
    #                   dpi=ppi, constrained_layout=True)
    fig2 = plt.figure(figsize=(figw / ppi, figh / ppi),
                      dpi=ppi)
    ax2 = fig2.add_subplot(1, 1, 1)
    ax2.fill_between(densarray[0, :]*10000, ones, 0.8*ones, alpha=0.2)
    ax2.fill_between(densarray[0, :]*10000, 0.2*ones, 0*ones, alpha=0.2)

    linestyles = ['solid', (0, (1,1)), 'dashed', 'dashdot']
    for i, name in enumerate(names_sorted):
        color = get_color(E_b[i], vmin=vmin, vmax=vmax)
        cutoff = round(dens[i]*10000,1)
        linestyle = linestyles[i % len(linestyles)]
        if i <= N:
            label = r'$\mathrm{' + bilayers[i].replace('-H-','\mbox{-}').replace('-T-','\mbox{-}').replace('2','_2') + '}$ (' + str(cutoff) + ')'
            ax.plot(densarray[i, :]*10000,
                    delta[i, :]*100,
                    linestyle=linestyle,
                    color=color,
                    linewidth=1,
                    label=label)
                    # label=bilayers[i])
            ax2.plot(densarray[i, :]*10000,
                     condfrac[i, :],
                     linestyle=linestyle,
                     color=color,
                     linewidth=1,
                     label=label)
                    #  label=bilayers[i])
        else:
            ax.plot(densarray[i, :]*10000,
                delta[i, :]*100,
                color=color,
                linestyle='dashed',
                linewidth=0.5)

            ax2.plot(densarray[i, :]*10000,
                    condfrac[i, :],
                    color=color,
                    linestyle='dashed',
                    linewidth=0.5)
    
    plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), orientation='vertical', label=r'$E_b$ [meV]')
    # ax.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=2)
    ax.legend(bbox_to_anchor=(-0.14,0.5), loc="center right")
    ax.set_xlabel(r'Density [10$^{12}$ cm$^{-2}$]')
    ax.set_ylabel('Gap [meV]')
    ax.set_xticks(np.arange(0, xmax, 5))
    ax.set_yticks(np.arange(0,20,5))
    ax.set_xlim([0, xmax])
    # legend = ax.legend(loc='lower right')
    # legend.remove()
    ax.grid()
    # fig.tight_layout()
    fig.savefig('./plots/deltamax_' + figname + postfix + '.png')
    fig.savefig('./plots/deltamax_' + figname + postfix + '.pdf')
    ax2.set_ylabel('Condensate fraction')
    ax2.set_xlabel(r'Density [10$^{12}$ cm$^{-2}$]')
    ax2.set_xticks(np.arange(0, xmax, 5))
    ax2.set_xlim([0, xmax])
    plt.text(xmax - 8*xmax/43, 0.87, 'BEC', fontsize=12)
    plt.text(xmax - 8*xmax/43, 0.07, 'BCS', fontsize=12)
    ax2.grid()
    fig2.tight_layout()
    fig2.savefig('./plots/condfrac_' + figname + postfix + '.png')
    fig2.savefig('./plots/condfrac_' + figname + postfix + '.pdf')


# MAIN
# number of materials to label in figure.
# MATERIALS WITH N LARGEST CUTOFF DENSITIES WILL HAVE A LABBEL
N = 10
make_figure(figname='QEH', xmax=25, N=N, postfix='')
make_figure(figname='analytic',xmax=43,N=N, postfix='')

# %%
