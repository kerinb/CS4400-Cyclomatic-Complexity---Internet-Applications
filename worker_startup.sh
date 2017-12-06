max=$1
echo "max: $max"
for i in {0..$max}
do
    echo "$i"
    python Worker.py &
done
wait