# README #
# Birmingham Parallel Genetic Algorithm (BPGA).

### Installation ###

To download the BPGA you need Git installed on your computer. If Git is installed use the following command: 

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

Create a new directory and add the following files - 

```
#!shell

INCAR
KPOINTS
POTCAR 
Run.py
Sub.sh
```

Ensure your submission script contains the following line - 

```
#!shell

python Run.py
```

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