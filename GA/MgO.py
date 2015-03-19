'''
Generate MgO surface.

Jack Davis

16/1/15
'''

class MgO():

    def __init__(self,x,y,z,vac):

        self.xyz = []

        self.x = x
        self.y = y
        self.z = z

        self.vac = vac

        self.lat = 4.212

    def getSurf(self):

        self.genX()
        self.genY()
        self.genZ()

        return self.xyz

    def genX(self):

        for i in range(self.x):

            x = i * self.lat / 2
            y = 0.0
            z = 0.0 

            if i % 2 != 0:
                line = ["Mg",x,y,z]
            else:
                line = ["O",x,y,z]

            self.xyz.append(line)

    def genY(self):

        natoms = len(self.xyz)

        for i in range(1,self.y):
            for j in range(natoms):

                ele,x,y,z = self.xyz[j]

                if ele == "Mg":
                    if i % 2 != 0:
                        ele = "O"
                elif ele == "O":
                    if i % 2 != 0:
                        ele = "Mg"

                y += i * (self.lat / 2) 

                newline = [ele,x,y,z]
                self.xyz.append(newline)

    def genZ(self):

        natoms = len(self.xyz)

        for i in range(1,self.z):
            for j in range(natoms):

                ele,x,y,z = self.xyz[j]

                if ele == "Mg":
                    if i % 2 != 0:
                        ele = "O"
                elif ele == "O":
                    if i % 2 != 0:
                        ele = "Mg"

                z += i * (self.lat / 2) 

                newline = [ele,x,y,z]
                self.xyz.append(newline)
