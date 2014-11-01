'''
Generate Random Pool

Jack Davis

10/10/14
'''

import random as ran
import os

class ranPool:

    def __init__(self,n,r_ij,eleNums,eleNames):

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

        r_ij = 3.0
        scale = self.natoms**(1./3.)

        natoms = self.natoms
        eleNames = self.eleNames
        eleNums = self.eleNums

        with open("pool.dat","w") as pool:
            for struc in range(self.nstrucs):
                pool.write(str(natoms) + "\n")
                pool.write("NotMinimised " + str(struc+1) + "\n")
                for i in range(len(eleNames)):
                    for j in range(eleNums[i]):
                        x = ran.uniform(0,1) * self.r_ij * scale
                        y = ran.uniform(0,1) * self.r_ij * scale
                        z = ran.uniform(0,1) * self.r_ij * scale
                        xyz = str(x) + " " + str(y) + " " + str(z) + "\n"
                        line = eleNames[i] + " " + xyz
                        pool.write(line)
