'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
The Johnston Group

10/7/15

--- BPGA Example Input File ---

A calculation requires the following
VASP input files:

1 - INCAR
2 - KPOINTS
3 - POTCAR 

---

'''

import GA.Input as In

from GA.MgO import MgO 
from GA.NewPoolGA import poolGA

nPool = 10
mutType = "homotop"
cross = "weighted"
mutate = 0.1
r_ij = 3.0
eleNums = [2,2]
eleNames = ["Au","Pd"]
eleMasses = In.masses(eleNames)
natoms = sum(eleNums)
boxAdd = 10.0

subString = "aprun -n 24 vasp5.gamma > output.dat"

'''--- Surface GA ---'''

surfGA = False

'''
Define surface object.
'''

surface = MgO(x=4,y=4,z=2,vac=6,clusHeight=1.)

''' ---------------- '''

In.checkFiles()

StartCalc = poolGA(natoms,r_ij,eleNums
    			,eleNames,eleMasses,mutate,nPool
			    ,cross,mutType,subString,boxAdd
			    ,surface,surfGA)
