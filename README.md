# README #
# Birmingham Parallel Genetic Algorithm (BPGA).

### Installation ###

To download the BPGA you need Git installed on your computer. If Git is installed use the following command to download the BPGA: 

```
#!shell

git clone https://bitbucket.org/JBADavis/bpga.git
```

then add the following line to your ~/.bashrc file:

```
#!shell

export PYTHONPATH=$PYTHONPATH:~/bpga
```

### Serial Jobs ###

Calculations must be run in separate directories, each of which must contain the following files:

```
#!shell

INCAR
KPOINTS
POTCAR 
Run.py
```

Where the Run.py file is the BPGA's input script. An example calculation directorycan be found in:

```
#!shell

~/bpga/Examples/Au2Ir2 
```

To run a calculation on a different HPC change the subString variable in Run.py to the required command for a parallel VASP run:

```
#!python 

subString = "aprun -n 24 vasp5.gamma" 
```

### Selection 

Selection is currently only through roulette wheel selection. Tournament will be added again soon! 

### Crossover 

Deaven and Ho 1pt crossover can be performed with either a random or weighted cutting plane:

```
#!shell

cross = "random"
cross = "weighted"
```

The weighted plane is determined by fitness of the two clusters selected for crossover. 

### Mutation 

The available mutation methods available are: 

```
#!shell

mutType = "random"
mutType = "move"
mutType = "homotop" 
```

## random 