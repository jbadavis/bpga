'''
Write POSCAR

Jack Davis

19/1/15
'''

import os

class surfacePOSCAR():

    def __init__(self
                ,calcNum
                ,slabClusXYZ
                ,surface):

        self.calcNum = str(calcNum)

        self.xyz = slabClusXYZ

        self.x = surface.x
        self.y = surface.y
        self.z = surface.z
        self.vac = surface.vac
        self.lat = surface.lat

        self.box = 0.

        self.eleNums = []

        self.getSurfEle()
        self.getEleNums()

        self.printPOSCAR()

    def getSurfEle(self):

        self.eleNames=[]

        for i in self.xyz:
            ele,x,y,z = i
            if ele not in self.eleNames:
                self.eleNames.append(ele)

    def getEleNums(self):

        for element in self.eleNames:
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

            for element in self.eleNames:
                poscar.write(element+" ")

            poscar.write("\n")

            for eleNum in self.eleNums:
                poscar.write(str(eleNum)+" ")

            # Selective dynamics.
            poscar.write("\nS\n")

            # Cartesian Coordinates.
            poscar.write("C\n")

            for element in self.eleNames:
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

    # def printXYZ(self):

    #     '''
    #     For testing
    #     '''

    #     with open("XYZ","a") as xyzfile:

    #         xyzfile.write(str(len(self.xyz))+"\n\n")

    #         for i in self.xyz:
    #             ele,x,y,z = i 
    #             line = ele+" "+str(x)+" "+str(y)+" "+str(z)+"\n"
    #             xyzfile.write(line)
