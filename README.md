# DFT-project: Exciton Superfluids
Project for calculating parameters for a more realistic modelling of exciton superfluids in 2D Heterostructures.

## Getting Started

### Install dependencies
Dependencies are listed in requirements.txt. Run the following command to install the python packages
```
pip install -r requirements.txt
```

## Usefull commands specific to the dtu gbar hpc environment
### Load in intel compiler module
```
module add intel
```
### Queuing tasks/jobs
Navigate to repo folder on gbar. Then you can run the following:
- Submit job on 8 cores for 4 hours
```
mq submit script.py -R 8:4h
```

- Submit job `WSe2_bb.py` after `WSe2_gs.py` has completed:
```
mq submit WSe2_bb.py -d WSe2_gs.py -R 8:4h
```

- List jobs
```
mq ls
```

- Remove job
```
mq rm -i JOBID
```

- Help
```
mq help
```

- Help on command (e.g. rm command)
```
mq rm -h
```


### General commands (from startup guide)
- Login with Forward X11 (use dtu user password)
```
ssh -XY USERNAME@login.gbar.dtu.dk
```

- Log onto a compute node
```
linuxsh -X
```

- Create virtual environment: Follow instructions [here](https://wiki.fysik.dtu.dk/gpaw/platforms/gbar/gbar.html)
- Activate virtual environemtn (you can add this to your `.bashrc`)
```
source ~/path-to-your-venv/bin/activate
```

- Launch interactive jupyter notebook
```
python -m ipykernel install --user --name=your-venv
jupyter notebook --no-browser --port 40000 --ip=$HOSTNAME
```
Open new terminal locally and run (USERNAME: your DTU username, HOSTNAME: servername you see in the other window (n-XX- YY-ZZ), PORT: 40000)
```
ssh USERNAME@login.gbar.dtu.dk -g -L8080:HOSTNAME:PORT -N
```
Go into your browser and open: http://localhost:8080. When you are creating a new note notebook on the web browser, go to “new” and then choose the name of your virtual environment to make it work. If you already have written the notebook, just go to “kernel” -> “change kernel” and choose your respective environment.