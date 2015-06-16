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
sub.sh
```

An example calculation for the BlueBEAR HPC can be found in:

```
#!shell

~/bpga/Examples/Au2Ir2 

### Crossover 

Available crossover methods - 

```
#!shell

cross = "random"
cross = "weighted"
cross = "bimetallic" 
```

"random" chooses a random cutting plane whereas for "weighted" this is determined by the fitness.

Random also works for bimetallics.

Currently bimetallic crossover takes 50% from each cluster.

### Mutation 

Available mutation methods - 

```
#!shell

mutType = "random"
mutType = "move"
mutType = "homotop" 
```

"Random" generates an entirely new geometry. "Move" randomly displaces two atoms within the cluster. "homotop" is a bimetallic mutation, where the atoms types are shuffled.