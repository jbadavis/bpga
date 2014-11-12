'''
Generate Random Pool

Jack Davis

10/10/14
'''

import os
import random as ran

from Explode import checkClus

class ranPool:

    def __init__(self,n,r_ij
        ,eleNums,eleNames):

        ran.seed()

        self.nstrucs = n
        self.r_ij = r_ij
        self.natoms = 0
        self.eleNums = eleNums
        self.eleNames = eleNames
        
        for i in self.eleNums:
            self.natoms += i

        popExists = os.path.exists("pool.dat")

        if popExists == False:
            self.genPool()

    def genPool(self):

        '''
        Generates initial
        random population
        database.
        '''

        scale = self.natoms**(1./3.)

        for struc in range(self.nstrucs):

            noOverlap = True

            while noOverlap:
                
                coords=[]

                for i in range(self.natoms*3):
                    coords.append(ran.uniform(0,1)*self.r_ij*scale) 

                check = checkClus(self.natoms,coords)

                noOverlap = check.overlap()

            coords = [coords[i:i + 3] for i in range(0, len(coords), 3)]

            with open("pool.dat","a") as xyzFile:
                c = 0
                xyzFile.write(str(self.natoms)+"\n")
                xyzFile.write("NotMinimised\n")
                for i in range(len(self.eleNames)):
                    for j in range(self.eleNums[i]):
                        xyz = coords[c]
                        xyz = [str(k) for k in xyz]
                        xyzLine = xyz[0]+" "+xyz[1]+" "+xyz[2]+"\n"
                        xyzlineEle = self.eleNames[i] + " " + xyzLine
                        xyzFile.write(xyzlineEle)
                        c += 1
