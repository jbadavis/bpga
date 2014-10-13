'''
Main Algo

Jack Davis

10/10/14
'''

import pop
import minimiser

npool = 10

newPool = pop.ranPool(npool)

natoms = newPool.natoms

minimise = minimiser.minimiser(natoms,npool)
