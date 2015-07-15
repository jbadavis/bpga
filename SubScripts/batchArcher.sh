#!/bin/bash --login
#PBS -r y
#PBS -N BPGA
#PBS -l select=8
#PBS -l walltime=8:00:0
#PBS -A e05-react-roy

export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)
cd $PBS_O_WORKDIR
base=$PBS_O_WORKDIR

module load vasp5

# Specify the number of parallel instances.
instances=4 

# For multiple compositions add directory 
# names to first loop
for i in Au2Rh2 ; do 
  # Do not change! 
  cd $base/$i 
  for (( j=1; j<=$instances; j++)); do 
    python Run.py &
    sleep 10
  done
done

wait
