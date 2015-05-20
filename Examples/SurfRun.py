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
mutType = "move" # move, random, homotop or surface. 
cross = "weighted"
mutate = 0.2
r_ij = 3.0
eleNums = [4]
eleNames = ["Au"]
eleMasses = In.masses(eleNames)
natoms = sum(eleNums)

boxAdd = 10.0

subString = "aprun -n 24 vasp5.gamma > output.dat"

'''--- Surface GA ---'''

surfGA = True

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
    ,cross,mutType,subString,boxAdd
    ,surface,surfGA)
