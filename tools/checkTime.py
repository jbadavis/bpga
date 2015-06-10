import sys, os

completeCount = 0
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
