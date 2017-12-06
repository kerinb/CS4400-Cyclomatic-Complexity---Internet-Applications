#!/usr/bin/python
for i in (1..sys.argv[1])
do
    echo "value $i"
    python Worker.py &
done
wait