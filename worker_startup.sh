#!/usr/bin/python
for i in {1..$1}
do
    python Worker.py &
done
wait