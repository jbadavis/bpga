''' 
Minimise Mutant

Jack Davis

20/10/14
'''

import os
import random as ran

import Database as db

from DFT_input import vasp_input as DFTin
from DFT_output import vasp_output as DFTout

from checkPool import checkPool as checkPool
from CoM import CoM 

from fixOverlap import fixOverlap
from Explode import checkClus

class minMut: 

	def __init__(self,natoms,r_ij
		,mutType,eleNums,eleNames
		,eleMasses,n,stride
		,subString):

		self.natoms = natoms
		self.r_ij = r_ij
		self.mutType = mutType
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.n = n
		self.stride = stride
		self.subString = subString

		ran.seed()

		self.runCalc()

	def runCalc(self):

		db.lock()

		self.xyzNum = db.findLastDir() + 1

		if self.mutType == "random":
			self.randomMutate()
		elif self.mutType == "move":
			self.moveMutate()

		os.system("mkdir " + str(self.xyzNum))
							
		db.unlock()

		self.minimise()

	def restart(self):

		'''
		Restart Calculation
		without making 
		new directory.
		'''

		db.lock()

		if self.mutType == "random":
			self.randomMutate()
		elif self.mutType == "move":
			self.moveMutate()

		db.unlock()

		self.minimise()

	def randomMutate(self):

		scale = self.natoms**(1./3.)

		coords=[]

		for i in range(self.natoms*3):
			coords.append(ran.uniform(0,1)*self.r_ij*scale) 

		self.writeXYZ(coords)

	def moveMutate(self):

		'''
		Pick random 
		structure 
		from pool and 
		displace two
		atoms.
		'''

		coords=[]

		ranStruc=ran.randrange(0,self.n)
		ranAtom=ran.randrange(0,self.natoms)
		ranPoolPos=ranStruc*self.stride

		poolList = db.readPool()

		clus=poolList[ranPoolPos:ranPoolPos+self.stride]
		clus=clus[2:]

		for i in ran.sample(range(0,self.natoms),2):
			ranCoods=clus[i]
			ele,x,y,z=ranCoods.split()
			ranX=float(x)+ran.uniform(-1.,1.)
			ranY=float(y)+ran.uniform(-1.,1.)
			ranZ=float(z)+ran.uniform(-1.,1.)
			ranLine=ele+" "+str(ranX)+" "+str(ranY)+" "+str(ranZ)+"\n"
			clus[ranAtom]=ranLine

		for line in clus:
			ele,x,y,z = line.split()
			coords.append(float(x))
			coords.append(float(y))
			coords.append(float(z))

		self.writeXYZ(coords)	

	def moveRotate(self):

		'''
		Rotate half 
		a cluster.
		'''

		pass

	def writeXYZ(self,coords):	

		coordsFix = fixOverlap(coords)
		coordsFix = [coordsFix[i:i + 3] for i in range(0, len(coordsFix), 3)]

		with open(str(self.xyzNum)+".xyz","w") as xyzFile:
			c = 0
			xyzFile.write(str(self.natoms)+"\n")
			xyzFile.write("Mutant\n")
			for i in range(len(self.eleNames)):
				for j in range(self.eleNums[i]):
					xyz = coordsFix[c]
					xyz = [str(k) for k in xyz]
					xyzLine = xyz[0]+" "+xyz[1]+" "+xyz[2]+"\n"
					xyzlineEle = self.eleNames[i] + " " + xyzLine
					xyzFile.write(xyzlineEle)
					c += 1	

	def minimise(self):

		'''
		Start 
		DFT calculation.
		'''

		self.vaspIN = DFTin(self.xyzNum,self.eleNames
						,self.eleMasses,self.eleNums)

		if self.doDFT() == 0:

			output = DFTout(self.xyzNum,self.natoms)

			if output.checkError():
				self.restart()
			else:
				self.finalEnergy = output.getEnergy()
				self.finalCoords = output.getCoords()

				check = checkClus(self.natoms,self.finalCoords)

				if check.exploded() == False:
					self.updatePool()
				else:
					self.restart()

	def doDFT(self):

		'''
		Change directory and 
		submit calculation.
		'''

		base = os.environ["PWD"]
		os.chdir(base+"/"+str(self.xyzNum))

		exitcode = os.system(self.subString)

		with open(base+"/exitcodes.dat","a") as exit:
			exit.write(str(self.xyzNum))
			exit.write(" Exitcode = "+str(exitcode)+"\n")
			
		os.chdir(base)

		return exitcode

	def updatePool(self):

		AcceptReject = checkPool()
		Accept = AcceptReject.checkEnergy(float(self.finalEnergy))

		if Accept:
			Index = AcceptReject.lowestIndex
			Index = (Index*self.stride)+1

			db.updatePool("Finish"
				,Index,self.eleNums,
				self.eleNames,self.eleMasses
				,self.finalEnergy,self.finalCoords
				,self.stride,self.vaspIN.box)
