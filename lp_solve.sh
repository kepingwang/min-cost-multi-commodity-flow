if [ $# -eq 0 ]
  then
    echo "input the .net filename"
fi

echo "======== The LP ========"
python3 lp/gen_lp.py $1
echo "======== Solving the LP ========"
cplex -c "read $1.lp" "optimize" "display solution variables 1-" | tee $1.lp.sol
