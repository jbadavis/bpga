'''
Database operations.

Jack Davis

5/11/2014
'''

import os
import time

from CoM import CoM 

def updatePool(upType,strucNum
	,eleNums,eleNames,eleMasses
	,finalEn,finalCoords
	,stride,box):

	'''
	After completion take
	final energy and coords
	from OUTCAR and Update
	poolList
	'''

	check()
	lock()

	poolList = readPool()

	coordsEle=addEle(upType,finalCoords
		,eleNums,eleNames,eleMasses,box)

	poolList[strucNum+1:strucNum+stride-1]=coordsEle

	if "Finish" in upType:
		poolList[strucNum]="Finished Energy = "+str(finalEn)+"\n"
	elif "Restart" in upType:
		poolList[strucNum]="Restart\n"

	writePool(poolList)

	unlock()

def addEle(upType,coords
	,eleNum,eleNames
	,eleMasses,box):

	'''
	Adds element types 
	to final coordinates
	from OUTCAR. Removes 
	from centre of box
	'''

	eleList=[]
	coordsEle=[]

	if "Finish" in upType:
		coords = [float(i) - box/2 for i in coords]

	coords = [str(i) for i in coords]

	for i in range(len(eleNames)):
		for j in range(eleNum[i]):
			eleList.append(eleNames[i])

	for i in range(0,len(coords),3):
		xyz=coords[i]+" "+coords[i+1]+" "+coords[i+2]+"\n"
		xyzLine=eleList[i/3]+" "+xyz
		coordsEle.append(xyzLine)

	coordsEle = CoM(coordsEle,eleNames,eleMasses)

	return coordsEle


def findLastDir():

	'''
	Finds directory
	containing last
	calculation.
	'''

	calcList = []
	dirList = os.listdir(".")

	for i in dirList:
		try:
			calcList.append(int(i))
		except ValueError:
			continue

	calcList = sorted(calcList)

	lastCalc = calcList[len(calcList)-1]

	return lastCalc

def readPool():

	'''
	Reads pool at beginning/
	throughout calculation.
	'''

	with open("pool.dat","r") as pool:
		poolList = pool.readlines()

	return poolList

def writePool(poolList):

	'''
	Writes pool to
	file after any
	changes.
	'''

	with open("pool.dat","w") as pool:
		for line in poolList:
			pool.write(line)

def lock():

	os.system("touch lock.db")

def unlock():

	os.system("rm lock.db")

def check():

	while os.path.exists("lock.db"):
		time.sleep(0.5)
		