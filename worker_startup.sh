#!/bin/bash

for i in $1
do
    echo "value $i"
    python Worker.py &
done
wait