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
mutType = "move"
cross = "weighted"
mutate = 2
r_ij = 3.0
eleNums = [4,4]
eleNames = ["Pt","Rh"]
eleMasses = In.masses(eleNames)
natoms = sum(eleNums)

subString = "aprun -n 24 vasp5.gamma"

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

StartCalc = poolGA(natoms,r_ij,eleNums
	,eleNames,eleMasses,mutate,npool
	,cross,mutType,subString)