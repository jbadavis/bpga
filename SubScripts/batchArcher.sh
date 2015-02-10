#!/bin/bash --login
#PBS -r y
#PBS -N GA
#PBS -l select=2
#PBS -l walltime=12:00:0
#PBS -A e05-react-roy

export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)
cd $PBS_O_WORKDIR

module load vasp5

# Stops job if program crashes
# and begins running on the 
# launcher nodes. 
ulimit -t 3600

for i in {1..2}; do
  python Run.py &
  sleep 10
done

wait
