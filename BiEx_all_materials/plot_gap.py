
from os import path, chdir
chdir(path.dirname(path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

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


def make_figure(figname, xmax, N):
    ppi = 100
    figw = 600
    figh = 450
    SMALL_SIZE = 10
    MEDIUM_SIZE = 12
    plt.rc('font', size=SMALL_SIZE)
    plt.rc('axes', titlesize=SMALL_SIZE)
    plt.rc('axes', labelsize=MEDIUM_SIZE)
    plt.rc('xtick', labelsize=MEDIUM_SIZE)
    plt.rc('ytick', labelsize=MEDIUM_SIZE)
    plt.rc('legend', fontsize=SMALL_SIZE)
    plt.gcf().subplots_adjust(bottom=0.15)

    dens = []
    densarray = []
    delta = []
    condfrac = []

    filenames = Path('out').glob('n-*'+figname+'_MF/DeltaN_MF_iTemp001')
    names = []
    for i, filename in enumerate(filenames):
        fn = str(filename)
        tmp, tmp2, tmp3, tmp4 = load_Deltak(fn)
        name = fn.split('/')[1]
        names.append(name)
        dens.append(tmp)
        densarray.append(tmp2)
        delta.append(tmp3)
        condfrac.append(tmp4)

    plot_index = sorted(range(len(dens)), key=lambda sub: dens[sub])[-N:]

    dens = np.array(dens)
    densarray = np.array(densarray)
    delta = np.array(delta)
    condfrac = np.array(condfrac)
    ones = np.ones(densarray.shape[1])

    fig = plt.figure(figsize=(figw / ppi, figh / ppi),
                     dpi=ppi, constrained_layout=True)
    ax = fig.add_subplot(1, 1, 1)
    fig2 = plt.figure(figsize=(figw / ppi, figh / ppi),
                      dpi=ppi, constrained_layout=True)
    ax2 = fig2.add_subplot(1, 1, 1)
    ax2.fill_between(densarray[0, :]*10000, ones, 0.8*ones, alpha=0.2)
    ax2.fill_between(densarray[0, :]*10000, 0.2*ones, 0*ones, alpha=0.2)

    for i, name in enumerate(names):
        ax.plot(densarray[i, :]*10000,
                delta[i, :]*100,
                color='black',
                linestyle='dashed',
                linewidth=0.8)

        ax2.plot(densarray[i, :]*10000,
                 condfrac[i, :],
                 color='black',
                 linestyle='dashed',
                 linewidth=0.8)
        if i in plot_index:
            ax.plot(densarray[i, :]*10000,
                    delta[i, :]*100,
                    linestyle='solid',
                    linewidth=1.5, label=name)
            ax2.plot(densarray[i, :]*10000,
                     condfrac[i, :],
                     linestyle='solid',
                     linewidth=1.5, label=name)

    ax.legend()
    ax.set_xlabel(r'Density (10$^{12}$ cm$^{-2}$)')
    ax.set_ylabel('Gap (meV)')
    ax.set_xlim([0, xmax])
    legend = ax.legend(loc='lower right')
    legend.remove()
    ax.grid()
    fig.savefig('./plots/deltamax_'+figname+'.png')
    fig.savefig('./plots/deltamax_'+figname+'.pdf')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Condensate fraction')
    ax2.set_xlabel(r'Density (10$^{12}$ cm$^{-2}$)')
    ax2.set_xlim([0, xmax])
    plt.text(1, 0.8, 'BEC', fontsize=12)
    plt.text(1, 0.1, 'BCS', fontsize=12)
    ax2.grid()
    fig2.savefig('./plots/condfrac_'+figname+'.png')
    fig2.savefig('./plots/condfrac_'+figname+'.pdf')


# MAIN
# number of materials to label in figure.
# MATERIALS WITH N LARGEST CUTOFF DENSITIES WILL HAVE A LABBEL
N = 10
make_figure(figname='QEH', xmax=20, N=N)
make_figure(figname='analytic',xmax=20,N=N)
