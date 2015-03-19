#
# Finds lowest energy structures
# from a BPGA search.
#
# Jack Davis
# 18/3/15

base=$PWD

# Number of directories to search.
nstrucs=58

# Number of energies to print out.
nPrint=10

# -------------------------------#

echo "Searching $nstrucs directories."
echo "$nPrint lowest energy structures."

for ((  i=1; i <= $nstrucs; i++ )) ; do
  cd $base/$i
  energy=$(grep -a 'energy(sigma->0) =' OUTCAR | tail -1 | awk '{print $7}' )
  echo $i $energy
done | sort -k2n | head -$nPrint