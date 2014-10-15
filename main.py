'''
Main Algo

Jack Davis

10/10/14
'''

import GA.pop as pop
import GA.minimiser as minimiser

npool = 10
eleNums = [2,2]
eleNames = ["Ir","Pd"]

newPool = pop.ranPool(npool,eleNums,eleNames)

natoms = newPool.natoms

minimise = minimiser.minimiser(natoms,npool)
