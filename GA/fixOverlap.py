'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
The Johnston Group

27/4/15

--- FixOverlap Method ---

'''

import numpy as np

def fixOverlap(coords):

	overlaped = True

	while overlaped:

		overlaped = False

		for i in range(len(coords)):
			for j in range(len(coords)):

				x = coords[i][1] - coords[j][1]
				y = coords[i][2] - coords[j][2]
				z = coords[i][3] - coords[j][3]

				r=(np.sqrt((x**2)+(y**2)+(z**2)))

				if float("{0:.1f}".format(r)) < .9 and r != 0:
					
					diff = .9 - r
					coords[i][1] += diff
					coords[i][2] += diff
					coords[i][3] += diff

					overlaped = True

					break

	return coords