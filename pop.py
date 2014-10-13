'''
Generate Random Pool

Jack Davis

10/10/14
'''

import random as ran
import os

class ranPool:

    def __init__(self,n):

        ran.seed()

        self.nstrucs = n
        self.natoms = 0
        self.eleNums = [2,2]
        self.eleNames = ["Ir","Pd"]

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

        natoms = self.natoms
        eleNames = self.eleNames
        eleNums = self.eleNums

        with open("pool.dat","w") as pool:
            for struc in range(self.nstrucs):
                pool.write(str(natoms) + "\n")
                pool.write("Not Minimised" + "\n")
                for i in range(len(eleNames)):
                    for j in range(eleNums[i]):
                        x = ran.uniform(-1,1) * r_ij
                        y = ran.uniform(-1,1) * r_ij
                        z = ran.uniform(-1,1) * r_ij
                        xyz = str(x) + " " + str(y) + " " + str(z) + "\n"
                        line = eleNames[i] + " " + xyz
                        pool.write(line)
