#!/bin/bash

for i in $( seq 2 $1 ); do python Worker.py & done
python worker.py