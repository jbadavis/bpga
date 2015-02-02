'''
Generate Random Pool

Jack Davis

10/10/14
'''

import os
import random as ran

import Database as db

from fixOverlap import fixOverlap
from Explode import checkClus

class ranPool:

    def __init__(self,n,r_ij
                ,eleNums
                ,eleNames):

        ran.seed()

        self.nstrucs = n
        self.r_ij = r_ij
        self.natoms = 0
        self.eleNums = eleNums
        self.eleNames = eleNames
        
        for i in self.eleNums:
            self.natoms += i

        db.lock()

        if os.path.exists("pool.dat") == False:
            self.genPool()

        db.unlock()

    def genPool(self):

        '''
        Generates initial
        random population
        database.
        '''

        coords=[]

        scale = self.natoms**(1./3.)

        for i in range(self.nstrucs):
            for j in range(self.natoms*3):
                coords.append(ran.uniform(0,1)*self.r_ij*scale) 

        '''
        Generate list of
        element names.
        '''

        eleList=[]

        for i in range(len(self.eleNames)):
            for j in range(self.eleNums[i]):
                eleList.append(self.eleNames[i])

        '''
        Write pool.dat
        '''

        with open("pool.dat","w") as poolFile:
            for i in range(self.nstrucs):

                poolFile.write(str(self.natoms)+"\n")
                poolFile.write("NotMinimised\n")

                start = i * self.natoms*3
                finish = start + self.natoms*3
                clus = coords[start:finish]
                
                clus = fixOverlap(clus)
                clus = [str(i) for i in clus]

                for j in range(0,len(clus),3):

                    ele = eleList[j/3]
                    x = str(clus[j])
                    y = str(clus[j+1])
                    z = str(clus[j+2])

                    poolFile.write(ele+" "+x+" "+" "+y+" "+z+"\n")
                    