'''
Script for BPGA calculation analysis.

to run:
python checkTimes.py nDirs

Where nDirs is the number of directories in your 
calculation directory. 
'''

import sys, os

'''
Check the number of directories
is supplied.
'''	

if len(sys.argv) == 1: 
	print "- checkTimes requires the number of directories"
	print "  e.g. python checkTimes.py 50"
	sys.exit()

times = [] 

for i in range(1,int(sys.argv[1])+1):
  with open(str(i)+'/OUTCAR','r') as f:
    output = f.readlines()
    for line in output:
      if "Total CPU" in line:
        timeLine = line.split()
        times.append(float(timeLine[5]))

averageTime = sum(times) / float(len(times))

energiesDir = []

for i in range(1,int(sys.argv[1])+1):
  with open(str(i)+'/OUTCAR','r') as f:
	output = f.readlines()
  	for line1 in output:
	  	if "reached required accuracy" in line1:
	  		for line2 in output:
	  			if "energy  without entropy=" in line2:
	  				energyLine = line2.split()
	  				energy = energyLine[6]
	  				energyDir = [i,energy]
			energiesDir.append(energyDir)

energies = []

for calc in energiesDir:
	energies.append(calc[1])

minEnergy = max(energies)

for calc in energiesDir: 
	if minEnergy in calc[1]:
		minDir = calc[0]

print energiesDir

print "\n BPGA Run Analysis\n"

print " - Total Number of Completed Calculations: " + str( len(times) )
print " - Average Time per Calculation (secs): " + str( averageTime )
print " - Average Time per Calculation (mins): " + str( int(averageTime) / 60 )

print "\n Lowest Energy: " + minEnergy
print " Directory: " + str(minDir) + "\n" 
