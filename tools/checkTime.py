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
	print "checkTimes requires the number directories"
	print "python checkTimes.py 50"
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

print "Total Number of Calculations: " + str( len(times) )
print "Average Time (secs): " + str( averageTime )
print "Average Time (mins): " + str( int(averageTime) / 60 )

print "***"
print "Lowest Energy and Location: "
print "***"


