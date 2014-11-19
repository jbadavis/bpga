'''
Database operations.

Jack Davis

5/11/2014
'''

import os, time, errno

from CoM import CoM 

global fd

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

	'''
	An atomic operation on *most* OSes and filesystems
	Quote from man for open(2):
	
	"On NFS, O_EXCL is supported only when using NFSv3 or later on
	 kernel 2.6 or later.  In NFS environments where O_EXCL support
	 is not provided, programs that rely on it for performing
	 locking tasks will contain a race condition."
	'''

	global fd

	while True:

		try:
			fd = os.open('lock.db', os.O_CREAT|os.O_EXCL|os.O_RDWR)
			return

		except OSError as oserr:
			if oserr.errno == errno.EEXIST:
				time.sleep(0.5)	# Sleep for 500ms between polls
			else:
				raise

def unlock():

	global fd

	if (fd != None):
		os.close(fd)
		os.remove('lock.db')
		fd = None
	else:
		raise Exception("Attempted database unlock when not holding lock.")
		