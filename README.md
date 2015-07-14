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

### Crossover 

Available crossover methods:

```
#!shell

cross = "random"
cross = "weighted"
```

"random" chooses a random cutting plane whereas for "weighted" this is determined by the fitness.

### Mutation 

Available mutation methods: 

```
#!shell

mutType = "random"
mutType = "move"
mutType = "homotop" 
```

"Random" generates an entirely new geometry. "Move" randomly displaces two atoms within the cluster. "homotop" is a bimetallic mutation, where the atoms types are shuffled.