#!/bin/bash

for i in $1
do
    ./worker.py
done
wait