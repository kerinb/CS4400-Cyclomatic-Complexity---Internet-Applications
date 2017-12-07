#!/bin/bash
sleep 3

for i in $( seq 2 $1 ); do python Worker.py & done
python Worker.py