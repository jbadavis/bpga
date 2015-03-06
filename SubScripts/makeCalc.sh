#
# Creates GA Calc Directories 
# for a bimetallic system.

# Requires INCAR KPOINTS and BatchSub.sh

# Jack Davis 
# 6/3/15

natoms=6
eleA="Au"
eleB="Ir"

dirArray=()

echo "System = $natoms atom $eleA $eleB"

POTCARcat.sh $eleA $eleB

for (( i=0; i<=$natoms; i++)); do 

  j=$(( $natoms-$i ))
  dir=$eleA$i$eleB$j

  mkdir $dir

  dirArray+=( $dir )

  if [ $i -eq 0 ]; then
    eleNums="[$j]"
    eleNames="[$eleB]"
    mutType='"move"'
    cross='"weighted"'
  elif [ $j -eq 0 ]; then
    eleNums="[$i]"
    eleNames="[$eleA]"
    mutType='"move"'
    cross='"weighted"'
  else
    eleNums="[$i,$j]"
    eleNames="[$eleA,$eleB]"
    mutType='"homotop"'
    cross='"bimetallic"'
  fi

  sed -i "/mutType = */c\mutType = $mutType" Run.py
  sed -i "/cross = */c\cross = $cross" Run.py

  sed -i "/eleNames = */c\eleNames = $eleNames" Run.py
  sed -i "/eleNums = */c\eleNums = $eleNums" Run.py

  cp {KPOINTS,INCAR,POTCAR,Run.py} $dir
    
done

nCalc=${#dirArray[*]}

echo "Number of Calculations: $nCalc"

echo "Directories:"
for item in ${dirArray[*]}; do
  printf "  %s\n" $item
done

# 
# Change BatchSub.sh 
#

sed -i "/#PBS -l select=*/c\#PBS -l select=$nCalc" BatchSub.sh
sed -i "/for i in */c\for i in ${dirArray[*]} ; do" BatchSub.sh

