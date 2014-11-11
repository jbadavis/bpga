'''
Pool Genetic 
Algorithm

Jack Davis

10/10/14
'''

from GA.pop import ranPool
from GA.poolGA import poolGA
import GA.Input as In

npool = 10
mutate = 2
r_ij = 3.0
eleNums = [20]
eleNames = ["Au"]
eleMasses = In.masses(eleNames)
natoms = sum(eleNums)
hpc = In.hpc()
mpitasks = "24"

'''
If a pool.dat doesn't
already exist, pop
creates one.
'''

newPool = ranPool(npool,r_ij,eleNums,eleNames)

'''
Starts calculation by 
minimising pool and 
then producing offspring. 
'''

StartCalc = poolGA(natoms,r_ij,eleNums,eleNames
			,eleMasses,mutate,npool,hpc,mpitasks)
