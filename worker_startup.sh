max=$1
echo "max: $max"
for i in `seq 2 $max`
do
    echo "$i"
    python Worker.py
done
