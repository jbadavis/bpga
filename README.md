# README #
# Birmingham Parallel Genetic Algorithm (BPGA).

### Installation ###

Open your ~/.bashrc file and add the following line - 

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

"Random" chooses a random cutting plane whereas for "weighted" this is determined by the fitness.

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