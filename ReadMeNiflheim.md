# Usefull Commands specific to the Niflheim environment
Niflheim documentation: https://wiki.fysik.dtu.dk/niflheim/Niflheim7_Getting_started#jupyter-notebooks-on-niflheim

## Login nodes
- `slid.fysik.dtu.dk`: xeon24. 24 cores, 254 GB RAM. Run Jupyter Notebook on this node and start with queuing calculations here.
- `surt.fysik.dtu.dk`: xeon56. 56 cores, 512 GB RAM. Try queuing jobs here, if xeon24 fails.

## Configure MyQueue
```
mq config slurm | grep -v sm3090 > ~/.myqueue/config.py
```

## squeue commands
- View queue for your user
```
squeue -u $USER
```
- Detailed info on job
```
showjob <jobid>
```
- List of pending jobs in the same order considered for scheduling by Slurm:
```
squeue --priority --sort=-p,i --states=PD
```

## Modules
- List loaded modules
```
module list
```
- Check available modules (e.g. for GPAW)
```
module avail GPAW
```
- Load (temporarily "install") module
```
module load GPAW/<version>
```
- Run python code with module is at least possible with:
```
python3 <filename>.py
```

## GPAW on Niflheim
- presinstalled: https://wiki.fysik.dtu.dk/gpaw/platforms/Linux/Niflheim/load.html
- venv: https://wiki.fysik.dtu.dk/gpaw/platforms/Linux/Niflheim/build.html#id1

## Jupyter Notebook
- *Maybe you need to run `module avail IPython` and then load chosen version, e.g.*:
```
module load IPython/7.18.1-GCCcore-10.2.0
```
- Start jupyter server
```
jupyter notebook --no-browser
```
This outputs a Jupyter server address (e.g. http://127.0.0.1:8888/?token=xyz). Connect to the Jupyter Server as [described here](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server).
- Open up a jupyter notebook file (ipynb-file). In the top right corner, choose the remote venv kernel.