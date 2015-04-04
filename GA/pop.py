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

    def __init__(self
                ,nPool
                ,r_ij
                ,eleNums
                ,eleNames):

        ran.seed()

        self.nPool = nPool
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

        scale = self.natoms**(1./3.)

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

            for i in range(self.nPool):

                coords = []

                for j in range(self.natoms):
                    x = ran.uniform(0,1)*self.r_ij*scale
                    y = ran.uniform(0,1)*self.r_ij*scale
                    z = ran.uniform(0,1)*self.r_ij*scale
                    atom = [eleList[j],x,y,z]
                    coords.append(atom)

                coords = fixOverlap(coords)


                poolFile.write(str(self.natoms)+"\n")
                poolFile.write("NotMinimised\n")

                for j in range(0,len(coords)):

                    ele,x,y,z = coords[j]

                    line = ele+" "+str(x)+" "+str(y)+" "+str(z)+"\n"

                    poolFile.write(line)
                    