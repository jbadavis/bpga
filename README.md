# README #

Birmingham Parallel Pool GA (PPGA).

### Installation ###

Open your ~/.bashrc file and add the following line - 

```
#!shell

export PYTHONPATH=$PYTHONPATH:~/parallelbcga
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