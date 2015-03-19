#
# Create calculations for 
# a monometallic systems.
#
# Jack Davis 

# Requires INCAR KPOINTS POTCAR Run.py

nStart=10 
nFinish=20

base=$PWD

for (( i=$nstart; i=$nfinish; i++)); do
  dir="Au$i"
  mkdir $dir
  cp INCAR $dir
  cp KPOINTS $dir
  cp POTCAR $dir
  cp Run.py $dir
  natoms="[$i]" 
  sed -i "/eleNums = */c\eleNums = $natoms" $dir/Run.py
done
