'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
Jack Davis and the Johnston Group

20/3/15

--- Mutant Minimiser Class ---

'''

import os
import random as ran
import numpy as np

import Database as db

from DFT_input import vasp_input as DFTin
from DFT_output import vasp_output as DFTout

from checkPool import checkPool as checkPool
from CoM import CoM 

from fixOverlap import fixOverlap
from Explode import checkClus

from Crossover import crossover

# Surface GA
from SurfOpt import SurfOpt 
from surfacePOSCAR import surfacePOSCAR 

# Testing
import sys

class minMut: 

	def __init__(self,natoms,r_ij
				,mutType,eleNums,eleNames
				,eleMasses,n,stride
				,subString
				,surface,surfGA):

		self.natoms = natoms
		self.r_ij = r_ij
		self.mutType = mutType
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.n = n
		self.stride = stride
		self.subString = subString

		self.mutant = []

		'''
		Surface Object.
		'''

		self.surface = surface
		self.surfGA = surfGA

		''' --- ''' 

		ran.seed()

		self.runCalc()

	def runCalc(self):

		db.lock()

		self.xyzNum = db.findLastDir() + 1
		os.system("mkdir " + str(self.xyzNum))

		'''
		Mutation methods add to 
		mutant attribute. 
		'''

		if self.mutType == "surface" or self.surfGA:
			self.surfMutate()
		elif self.mutType == "random":
			self.randomMutate()
		elif self.mutType == "move":
			self.moveMutate()
		elif self.mutType == "homotop":
			self.homotopSwap()
							
		db.unlock()

		'''
		Minimise Mutant.
		'''

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

		for i in range(len(self.eleNames)):
			for j in range(self.eleNums[i]):

				ele = self.eleNames[i]

				x = ran.uniform(0,1)*self.r_ij*scale
				y = ran.uniform(0,1)*self.r_ij*scale
				z = ran.uniform(0,1)*self.r_ij*scale

				atom = [ele,x,y,z]

				self.mutant.append(atom)

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
		ranPoolPos=ranStruc*self.stride

		'''
		Number of atoms displace
		'''
		nMove = int(round(self.natoms*0.2))

		'''
		Get random cluster from pool.
		'''

		poolList = db.readPool()

		clus=poolList[ranPoolPos:ranPoolPos+self.stride]
		clus=clus[2:]

		for i in ran.sample(range(0,self.natoms),nMove):
			ranCoods=clus[i]
			ele,x,y,z=ranCoods.split()

			x=float(x)+ran.uniform(-1.,1.)
			y=float(y)+ran.uniform(-1.,1.)
			z=float(z)+ran.uniform(-1.,1.)

			ranLine=ele+" "+str(x)+" "+str(y)+" "+str(z)+"\n"
			clus[i]=ranLine

		for line in clus:
			ele,x,y,z = line.split()
			atom = [ele,float(x),float(y),float(z)]
			self.mutant.append(atom)

	def homotopSwap(self):

		'''
		Select cluster 
		from pool
		'''

		poolList = db.readPool()

		ranStruc=ran.randrange(0,self.n)
		ranPoolPos=ranStruc*self.stride

		clus = poolList[ranPoolPos:ranPoolPos+self.stride]
		clus = clus[2:]

		for i in range(len(clus)):
			ele,x,y,z = clus[i].split()
			atom = [ele,float(x),float(y),float(z)]
			clus[i] = atom

		'''
		Choose pair of different elements to swap.
		'''

		elementsMatch = True

		while elementsMatch:
			elementsMatch = False	
			pair = ran.sample(range(0,self.natoms),2)
			if clus[pair[0]][0] == clus[pair[1]][0]:
				elementsMatch = True 

		'''
		Swap element types of pair.
		'''

		temp = clus[pair[0]][0]
		clus[pair[0]][0] = clus[pair[1]][0]
		clus[pair[1]][0] = temp

		self.mutant = clus

	def surfMutate(self):

		'''
		Rotate the cluster 
		on a surface.
		'''

		ranStruc=ran.randrange(0,self.n)
		ranPoolPos=ranStruc*self.stride

		poolList = db.readPool()

		clus=poolList[ranPoolPos:ranPoolPos+self.stride]
		clus=clus[2:]

		theta = ran.uniform(0,np.pi*2)
		phi = ran.uniform(0,np.pi)

		rot11 = np.cos(phi)
		rot12 = 0.0
		rot13 = -np.sin(phi)
		rot21 = np.sin(theta)*np.sin(phi)
		rot22 = np.cos(theta)
		rot23 = np.sin(theta)*np.cos(phi)
		rot31 = np.cos(theta)*np.sin(phi)
		rot32 = -np.sin(theta)
		rot33 = np.cos(theta)*np.cos(phi)

		for i in range(len(clus)):
			ele, x, y, z = clus[i].split()
			x, y, z = float(x), float(y), float(z)
			rotX = str(rot11*x + rot12*y + rot13*z)
			rotY = str(rot21*x + rot22*y + rot23*z)
			rotZ = str(rot31*x + rot32*y + rot33*z)
			# New line after rotation. 
			newLine = ele+" " +rotX+" "+rotY+" "+rotZ+"\n"
			clus[i] = newLine

		self.surfMut = clus

	def minimise(self):

		'''
		Start 
		DFT calculation.
		'''

		if self.surfGA:

			SurfaceStruc = SurfOpt(self.surfMut,self.surface,self.eleNames,self.eleMasses)

			SurfClus = SurfaceStruc.placeClus()

			self.vaspIN = surfacePOSCAR(self.xyzNum,SurfClus,self.surface)

		else: 

			''' 
			Gasphase.

			XYZ file is already written
			- Should be changed! 

			'''
	
			self.vaspIN = DFTin(self.xyzNum,self.mutant,self.eleNames
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
			exit.write(" Exitcode = "+str(exitcode)+" Mutant\n")
			
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
