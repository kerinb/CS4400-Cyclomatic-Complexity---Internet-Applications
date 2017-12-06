#!bin/bash
for ((i = 1; i <= $1; i++))
do
    python Worker.py &
done
wait