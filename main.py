'''
Pool Genetic 
Algorithm

Jack Davis

10/10/14
'''

import GA.pop as pop
from GA.poolGA import poolGA as poolGA

npool = 10
eleNums = [2,2]
eleNames = ["Ir","Pd"]
eleMasses = [192.2,106.42]
mutate = 1
natoms = sum(eleNums)
hpc = "bluebear"
mpitasks = "24"

'''
If a pool.dat doesn't
already exist, pop
creates one.
'''

newPool = pop.ranPool(npool,eleNums,eleNames)

'''
Starts calculation by 
minimising pool and 
then producing offspring. 
'''

StartCalc = poolGA(natoms,eleNums,eleNames,eleMasses,mutate,npool,hpc,mpitasks)
