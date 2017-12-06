for i in {0..$1}
do
    echo "workers spawned $i"
    python Worker.py
done