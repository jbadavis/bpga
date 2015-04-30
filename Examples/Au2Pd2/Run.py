'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
Jack Davis and the Johnston Group

20/3/15

--- BPGA Input file ---

'''

from GA.pop import ranPool
from GA.poolGA import poolGA
import GA.Input as In

from GA.MgO import MgO 

npool = 10
mutType = "homotop" # move, random, homotop or surface. 
cross = "weighted" # random, weighted or bimetallic 
mutate = 0.1
r_ij = 3.0
eleNums = [2,2]
eleNames = ["Au","Pd"]
eleMasses = In.masses(eleNames)
natoms = sum(eleNums)

subString = "mpirun vasp"

'''--- Surface GA ---'''

surfGA = False

'''
Define surface object.
'''

surface = MgO(x=4,y=4,z=2,vac=6)

''' ---------------- '''

In.checkFiles()

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
    ,cross,mutType,subString
    ,surface,surfGA)
