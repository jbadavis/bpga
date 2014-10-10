'''
Main Algo

Jack Davis

10/10/14
'''

import pop
import minimiser

newPool = pop.ranPool(10)

natoms = newPool.natoms

minimise = minimiser.minimiser(natoms)