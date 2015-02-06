#!/bin/bash
#MOAB -l "walltime=48:0:0,nodes=2:ppn=16"
#MOAB -j oe
#MOAB -N vasp-GA
#MOAB -q bbjohnston

cd "$PBS_O_WORKDIR"

module load apps/vasp

for i in {1..2}; do
  python Run.py &
  sleep 5
done

wait
