'''
Input for 
PoolGA

Jack Davis

4/11/14
'''

import sys

def masses(eleNames):

	eleMasses = []

	eles = {'Au': 196.97,
			'Ir': 192.22,
			'Pt': 195.8 ,
			'Pd': 106.42,
			'Rh': 102.91,
			'Ag': 107.81,}

	for sym in eleNames:
		eleMasses.append(eles[sym])

	return eleMasses

def checkFiles():

	inFiles = ["INCAR","POTCAR","KPOINTS"]

	for File in inFiles:
		try:
			fd = open(File)
		except IOError:
			raise Exception("No "+File+" File!")