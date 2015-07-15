'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
The Johnston Group

11/11/14

--- Input Class ---

'''

import sys

def masses(eleNames):

	eleMasses = []

	eles = {'Au': 196.97,
			'Ir': 192.22,
			'Pt': 195.8 ,
			'Pd': 106.42,
			'Rh': 102.91,
			'Ag': 107.81,
			'Ni': 58.7
			'Fe': 55.85
			'Zn': 65.39}

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