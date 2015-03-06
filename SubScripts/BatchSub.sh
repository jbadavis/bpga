#!/bin/bash --login
#PBS -r y
#PBS -N GA
#PBS -l select=7
#PBS -l walltime=1:00:0
#PBS -A e05-react-roy

export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)
cd $PBS_O_WORKDIR

module load vasp5

#ulimit -t 3600

base=$PBS_O_WORKDIR

for i in Au0Ir6 ; do
  cd $base/$i
  python Run.py & 
done

wait
