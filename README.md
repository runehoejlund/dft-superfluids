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

- Launch interactive jupyter notebook (replace `venv` with name of your virtual environment)
```
python -m ipykernel install --user --name=venv
jupyter notebook --no-browser --port 40000 --ip=$HOSTNAME
```
Open new terminal locally and run (USERNAME: your DTU username, HOSTNAME: servername you see in the other window (n-XX- YY-ZZ), PORT: 40000)
```
ssh USERNAME@login.gbar.dtu.dk -g -L8080:HOSTNAME:PORT -N
```
Go into your browser and open: http://localhost:8080. When you are creating a new note notebook on the web browser, go to “new” and then choose the name of your virtual environment to make it work. If you already have written the notebook, just go to “kernel” -> “change kernel” and choose your respective environment.

### Git Commands
Note: You need to have cloned the repo and logged in with git to run the following commands. Checkout a beginner's guide to git, if you are unfamiliar with it.
- Check which files/folders have been modified.
```
git status
```
- View changes for a spceific file. (This command opens up a `less` editor/program. Type `h` for help and `q` to exit).
```
git diff [filename]
```
- Add modified file to "staging area" (i.e. tell git, that you intent to commit this modified file)
```
git add [filename]
```
- Add all modified files
```
git add *
```
- Commit added files
```
git commit -m "message"
```
- Push file to remote repository (**upload** changes)
```
git push
```
- Pull latest commits from remote repository (**download** latest changes)
```
git pull
```

### Running Jupyter Notebooks in VSCode
This may only work on a mac (unix system) because the X11-forwarding seems to be unsupported for VSCode on Windows. On the hpc compute node, run the following command:
- (optional) Set a password for the Jupyter Notebook Server:
```
jupyter notebook password
```
- Launch a Jupyer server with the following command:
```
jupyter notebook --no-browser --port 40000 --ip=$HOSTNAME
```
This outputs a Jupyter server address (e.g. http://n-10-10-1:40000/). Connect to the Jupyter Server as [described here](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#_connect-to-a-remote-jupyter-server) (don't include a token). Type the password when prompted to do so.
- Open up a jupyter notebook file (ipynb-file). In the top right corner, choose the remote venv kernel.