'''
Pool Genetic 
Algorithm

Jack Davis

10/10/14
'''

import GA.pop as pop
import GA.minimiser as minimiser

npool = 10
eleNums = [10,0]
eleNames = ["Ir","Pd"]
natoms = sum(eleNums)

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

minimise = minimiser.minimiser(natoms,npool)
