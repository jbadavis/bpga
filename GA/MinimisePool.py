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

--- Pool Minimiser Class ---

'''

import os
import time
import random as ran

import Database as db

from DFT_input import vasp_input as DFTin
from DFT_output import vasp_output as DFTout

from Select import tournamentSelect as select
from Crossover import crossover as cross 
from checkPool import checkPool as checkPool
from CoM import CoM 
from fixOverlap import fixOverlap
from Explode import checkClus

from SurfOpt import SurfOpt 
from surfacePOSCAR import surfacePOSCAR 

import sys

class minPool:

	def __init__(self,natoms,r_ij
				,eleNums,eleNames
				,eleMasses,n,stride
				,subString,boxAdd
				,surface,surfGA):
		
		self.natoms = natoms
		self.r_ij = r_ij
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.n = n
		self.stride = stride
		self.subString = subString
		self.boxAdd = boxAdd

		'''
		Surface Object.
		'''

		self.surface = surface
		self.surfGA = surfGA

		''' --- ''' 

		ran.seed()

		self.findStruc()

	def findStruc(self):

		self.strucNum = 0
			
		db.lock()

		self.poolList = db.readPool()

		for line in self.poolList:		
			
			self.xyzNum = (self.strucNum/self.stride)+1

			if os.path.exists(str(self.xyzNum)):
				time.sleep(0.5)
			
			if "NotMinimised" in line:

				self.poolList[self.strucNum] = "Running\n"

				os.system("mkdir "+str(self.xyzNum))

				db.writePool(self.poolList)
				db.unlock()

				self.getXYZ()
				self.minimise()
				break

			elif "Restart" in line:

				self.poolList[self.strucNum] = "Running\n"
				db.writePool(self.poolList)
				db.unlock()

				self.getXYZ()
				self.minimise()
				break

			self.strucNum += 1

		if os.path.exists("lock.db"): 
			db.unlock()

	def getXYZ(self):

		'''
		Grab structure 
		from pool.dat
		and write .xyz.
		'''

		clus = []

		strucNum=self.strucNum
		stride=self.stride
		
		clus = self.poolList[strucNum+1:strucNum+stride-1]

		for i in range(len(clus)):
			ele,x,y,z = clus[i].split()
			atom = [ele,float(x),float(y),float(z)]
			clus[i] = atom

		''' 
		Surface GA 

		If true place on surface. 
		 '''

		if self.surfGA:

			SurfaceStruc = SurfOpt(clus,self.surface,self.eleNames,self.eleMasses)

			surfClus = SurfaceStruc.placeClus()

			self.vaspIN = surfacePOSCAR(self.xyzNum,surfClus,self.surface)

		else: 

			'''
			Write POSCAR.
			'''
	
			self.vaspIN = DFTin(self.xyzNum,clus,self.eleNames
							,self.eleMasses,self.eleNums
							,self.boxAdd)


	def minimise(self):

		'''
		Start 
		DFT calculation.
		'''

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

		'''
		After completion take
		final energy and coords
		from OUTCAR and Update
		poolList
		'''

		db.updatePool("Finish"
			,self.strucNum,self.eleNums,
			self.eleNames,self.eleMasses
			,self.finalEnergy,self.finalCoords
			,self.stride,self.vaspIN.box)

	def restart(self):

		'''
		Generate new random geometry
		and update pool for restart.
		'''

		coords=[]

		scale=self.natoms**(1./3.)

		for i in range(len(self.eleNames)):
			for j in range(self.eleNums[i]):

				ele = self.eleNames[i]

				x = ran.uniform(0,1)*self.r_ij*scale
				y = ran.uniform(0,1)*self.r_ij*scale
				z = ran.uniform(0,1)*self.r_ij*scale

				atom = [ele,x,y,z]

				coords.append(atom)

		coords = fixOverlap(coords)

		''' 
		Remove element name 
		after fix.
		'''

		tempCoords=[]

		'''
		Remove elements and change 
		formating for update pool function. 
		'''

		for i in range(len(coords)):

			coords[i].pop(0)

			x,y,z = coords[i]

			tempCoords.append(x)
			tempCoords.append(y)
			tempCoords.append(z)

		coords = tempCoords

		finalEnergy = 0.

		db.updatePool("Restart"
			,self.strucNum,self.eleNums
			,self.eleNames,self.eleMasses
			,finalEnergy,coords
			,self.stride,self.vaspIN.box)
