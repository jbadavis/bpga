'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
Jack Davis and the Johnston Group

19/1/15

--- Surface POSCAR Class ---

'''

import os, sys

class surfacePOSCAR():

    def __init__(self
                ,calcNum
                ,eleNames
                ,slabClusXYZ
                ,surface):

        self.calcNum = str(calcNum)
        self.eleNames = eleNames
        self.eleNamesSurf = []

        self.addMgO()

        self.xyz = slabClusXYZ
        self.x = surface.x
        self.y = surface.y
        self.z = surface.z
        self.vac = surface.vac
        self.lat = surface.lat
        self.box = 0.
        self.eleNums = []

        self.getEleNums()

        self.printPOSCAR()

    def addMgO(self):

        for element in self.eleNames:
            self.eleNamesSurf.append(element)

        self.eleNamesSurf.append("O")
        self.eleNamesSurf.append("Mg")

    def getEleNums(self):

        '''
        Create a new, different eleNums 
        list containing cluster and slab.
        '''

        for element in self.eleNamesSurf:
            eleCount = 0
            for i in self.xyz:
                ele,x,y,z = i
                if ele == element:
                    eleCount += 1

            self.eleNums.append(eleCount)

    def printPOSCAR(self):

        xLat = str(self.x*(self.lat/2))
        yLat = str(self.y*(self.lat/2))
        zLat = str(self.z*(self.lat/2)+(self.vac * (self.lat/2)))

        with open("POSCAR","w") as poscar:

            poscar.write("Test\n")
            poscar.write("1.0\n")

            poscar.write( xLat +" 0.0 0.0\n")
            poscar.write("0.0 "+ yLat +" 0.0\n")
            poscar.write("0.0 0.0 "+ zLat +"\n")

            ''' Write elements '''

            for element in self.eleNamesSurf:
                poscar.write(element+" ")

            poscar.write("\n")

            for eleNum in self.eleNums:
                poscar.write(str(eleNum)+" ")

            '''
            Selective dynamics so that 
            the cluster relaxes and the 
            surface remains fixed.
            '''

            poscar.write("\nS\n")
            
            '''
            Use cartesian coordinates.
            '''

            poscar.write("C\n")

            '''
            Write coordinates in order of 
            element names. If the coordinates 
            belong to a cluster all the geometry 
            to relax. 
            '''

            for element in self.eleNamesSurf:
                for i in self.xyz:
                    ele,x,y,z = i
                    if ele == element:
                        if ele == "Mg" or ele == "O":
                            line = str(x)+" "+str(y)+" "+str(z)+" F F F\n"
                        else:
                            line = str(x)+" "+str(y)+" "+str(z)+" T T T\n"
                        poscar.write(line)
                        
        os.system("mv POSCAR "+self.calcNum)
        os.system("cp POTCAR "+self.calcNum)
        os.system("cp INCAR "+self.calcNum)
        os.system("cp KPOINTS "+self.calcNum)
