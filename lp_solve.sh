if [ $# -eq 0 ]
  then
    echo "input the .net filename"
fi

echo "======== The Graph ========"
cat $1
echo "======== The LP ========"
python3 lp/gen_lp.py $1 | tee $1.lp
echo "======== Solving the LP ========"
cplex -c "read $1.lp" "optimize" "display solution variables 1-" | tee $1.lp.sol
echo "======== Digraph LP ========"
python3 lp/gen_lp.py $1 -d | tee $1.d.lp
echo "======== Solving the Digraph LP ========"
cplex -c "read $1.d.lp" "optimize" "display solution variables 1-" | tee $1.d.lp.sol
