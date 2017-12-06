#!/bin/bash

for i in $( seq 2 $1 ); do python worker.py & done
python worker.py