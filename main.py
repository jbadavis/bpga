'''
Pool Genetic 
Algorithm

Jack Davis

10/10/14
'''

from GA.pop import ranPool
from GA.poolGA import poolGA

npool = 10
mutate = 1
r_ij = 2.0
eleNums = [2,2]
eleNames = ["Ir","Pd"]
eleMasses = [192.2,106.42]
natoms = sum(eleNums)
hpc = "bluebear" # archer/minerva
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
