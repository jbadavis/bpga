'''
Input for 
PoolGA

Jack Davis

4/11/14
'''

from subprocess import check_output

def hpc():

	host = check_output(['hostname'])

	if "bb2login" in host:
		return "bluebear"		
	elif "hpclogin" in host:
		return "minerva"
	elif "eslogin" in host:
		return "archer"
	elif "MacBook" in host:
		return "local"

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