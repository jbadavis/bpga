#!/bin/bash
#MOAB -l "walltime=12:0:0,nodes=1:ppn=16"
#MOAB -j oe
#MOAB -N vasp-GA

cd "$PBS_O_WORKDIR"

module load apps/vasp

python Run.py
