for i in $1
do
    echo "workers spawned $i"
    python Worker.py
done