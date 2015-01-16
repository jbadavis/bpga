# README #

This README would normally document whatever steps are necessary to get your application up and running.

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